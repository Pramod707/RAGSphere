from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct


class QdrantStroage:
    def __init__(self, url="http://localhost:6333", collection="docs", dim=1536):
        self.client = QdrantClient(url=url, timeout=20)
        self.collection = collection
        if not self.client.collection_exists():
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
            )

    def upsert(self, vectors, ids, playloads):
        points = [
            PointStruct(id=ids[i], vector=vectors[i], playload=playloads[i])
            for i in range(len(vectors))
        ]
        self.client.upsert(self.collection, points=points)

    def search(self, query_search, top_k: int = 5):
        result = self.client.search(
            collection_name=self.collection,
            query_vector=query_search,
            limit=top_k,
            with_payload=True,
        )

        contexts = []
        sources = set()

        for r in result:
            payload = getattr(r, "payload", None) or {}
            text = payload.get("text", "")
            source = payload.get("source", "")
            if text:
                contexts.append(text)
                sources.add(source)

        return {"context": contexts, "sources": list(sources)}
