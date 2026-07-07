from langchain_ollama import OllamaEmbeddings

embedding_model = OllamaEmbeddings(model="nomic-embed-text")

print(len(embedding_model.embed_query("hello")))
