from pydantic import BaseModel


class RAGChunkAndSrc(BaseModel):
    chunks: list[str]
    source_id: str


class RAGUpsertResult(BaseModel):
    ingest: int


class RAGSearchResult(BaseModel):
    context: list[str]
    sources: list[str]


class RAGQueryResult(BaseModel):
    answer: str
    sources: list[str]
    number_context: int
