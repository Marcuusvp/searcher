from fastapi import APIRouter
from pydantic import BaseModel
from app.services import embedding_service, vector_service, llm_service

router = APIRouter(prefix="/query", tags=["query"])


class QueryRequest(BaseModel):
    question: str


@router.post("")
async def query_documents(request: QueryRequest):
    query_embedding = embedding_service.generate_embedding(request.question)

    similar_chunks = vector_service.search_similar_chunks(
        query_embedding, match_count=5
    )

    if not similar_chunks:
        return {
            "answer": "Nenhum documento encontrado. Faça upload de PDFs primeiro.",
            "sources": [],
        }

    answer, sources = llm_service.generate_answer(request.question, similar_chunks)

    return {"answer": answer, "sources": sources}
