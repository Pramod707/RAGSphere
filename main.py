import logging
from fastapi import FastAPI
import uuid
import inngest
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
import inngest.fast_api
from inngest.experimental import ai
from data_loaders import embed_text, load_and_chunkPdf
from vector_db import QdrantStorage
from custom_type import RAGUpsertResult, RAGSearchResult, RAGChunkAndSrc, RAGQueryResult


inngest_client = inngest.Inngest(
    app_id="rag_app",
    logger=logging.getLogger("uvicorn"),
    is_production=False,
    serializer=inngest.PydanticSerializer(),
)


@inngest_client.create_function(
    fn_id="RAG : Ingest PDF", trigger=inngest.TriggerEvent(event="rag/ingest_pdf")
)
async def ingest_pdf(ctx: inngest.Context):
    def _load(ctx: inngest.Context) -> RAGChunkAndSrc:
        pdf_path = ctx.event.data["pdf_path"]
        source_id = ctx.event.data.get("source_id", pdf_path)
        chunks = load_and_chunkPdf(pdf_path)
        return RAGChunkAndSrc(chunks=chunks, source_id=source_id)

    def _upsert(chunk_and_src: RAGChunkAndSrc) -> RAGUpsertResult:
        chunks = chunk_and_src.chunks
        source_id = chunk_and_src.source_id
        vecs = embed_text(chunks)
        ids = [
            str(uuid.uuid5(uuid.NAMESPACE_URL, f"{source_id}:{i}"))
            for i in range(len(chunks))
        ]
        payload = [{"source": source_id, "text": chunks[i]} for i in range(len(chunks))]
        QdrantStorage().upsert(vecs, ids, payload)
        return RAGUpsertResult(ingest=len(chunks))

    chunk_and_src = await ctx.step.run(
        "load-and-chunk", lambda: _load(ctx), output_type=RAGChunkAndSrc
    )
    inggested = await ctx.step.run(
        "upsert", lambda: _upsert(chunk_and_src), output_type=RAGUpsertResult
    )
    return inggested.model_dump()


@inngest_client.create_function(
    fn_id="RAG : Query PDF",
    trigger=inngest.TriggerEvent(event="rag/query_pdf_ai"),
)
async def rag_query_pdf_ai(ctx: inngest.Context) -> RAGSearchResult:
    def _search(question: str, top_k: int = 5):
        query_vec = embed_text([question])[0]
        store = QdrantStorage()
        found = store.search(query_vec, top_k)
        return RAGSearchResult(context=found["context"], sources=found["sources"])

    question = ctx.event.data["question"]
    top_k = int(ctx.event.data.get("top_k", 5))
    found = await ctx.step.run(
        "embed-and-query", lambda: _search(question, top_k), output_type=RAGSearchResult
    )
    context_block = "\n\n".join(f"- {c}" for c in found.context)
    user_content = (
        f"Use the following context to answer the questions.\n\n"
        f"Context:\n{context_block}\n\n"
        f"Question:{question}"
        "Answer concisely using the context above."
    )

    llm = ChatOllama(model="qwen2.5:7b", temperature=0.2)

    res = llm.invoke(
        [
            SystemMessage(
                content="You answer questions using only the provided context."
            ),
            HumanMessage(content=user_content),
        ]
    )

    answer = res.content

    return {
        "answers": answer,
        "sources": found.sources,
        "number_context": len(found.context),
    }


#####################
app = FastAPI()


inngest.fast_api.serve(app, inngest_client, functions=[ingest_pdf, rag_query_pdf_ai])
