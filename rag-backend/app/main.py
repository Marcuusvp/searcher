from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import CORS_ORIGINS
from app.routers import upload, query
from app.services import vector_service

app = FastAPI(
    title="RAG Backend", description="Backend RAG para consulta de documentos internos"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[CORS_ORIGINS] if CORS_ORIGINS != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(query.router)


@app.get("/documents", tags=["documents"])
async def get_documents():
    documents = vector_service.get_all_documents()
    return {"documents": documents}


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}
