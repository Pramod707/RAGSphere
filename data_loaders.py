from llama_index.readers.file import PDFReader
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from llama_index.core.node_parser import SentenceSplitter

client = ChatOllama()
embedded_model = "qwen2.5:7b"
embed_dim = 1536
splitters = SentenceSplitter(chunk_size=1000, chunk_overlap=200)


def load_and_chunkPdf(path: str):
    docs = PDFReader().load_data(file=path)
    texts = [d.text for d in docs if getattr(d, "text", None)]
    chunks = []

    for t in texts:
        chunks.extend(splitters.split_text(t))

    return chunks


def embed_text(texts: list[str]) -> list[list[float]]:
    response = OllamaEmbeddings(model=embedded_model, inputs=texts)

    return [item.embeddings for item in response.data]
