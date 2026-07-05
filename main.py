import logging
from fastapi import FastAPI
import uuid
import inngest
import inngest.fast_api
from inngest.experimental import ai
import datetime
import os

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
    return {"hello world"}


#####################
app = FastAPI()

inngest.fast_api.serve(app, inngest_client, functions=[ingest_pdf])
