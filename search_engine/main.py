from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from utils import db_pipeline, convert_to_sentences

app = FastAPI(
    title="SearchPDF",
    version="0.1.0",
    docs_url=None,
    redoc_url="/docs"
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    search_result: str
    doc_id: List[int]
    sources: List[str]


@app.post("/search")
def search(requests: ChatRequest):

    contexts, context_ids, sources = db_pipeline(search_query=requests.message, collection_name="gto", update_index=False)
    context = convert_to_sentences(context_ids, sources, contexts)

    return ChatResponse(
        search_result=context,
        doc_id=context_ids,
        sources=sources
    )
