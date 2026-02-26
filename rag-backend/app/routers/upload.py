from fastapi import APIRouter, UploadFile, File, Form
from app.services import pdf_service, embedding_service, vector_service

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("")
async def upload_pdf(file: UploadFile = File(...), uploaded_by: str = Form(...)):
    if not file.filename.endswith(".pdf"):
        return {"status": "error", "message": "Only PDF files are supported"}

    file_bytes = await file.read()

    text = pdf_service.extract_text_from_pdf(file_bytes)

    chunks = pdf_service.chunk_text(text)

    embeddings = embedding_service.generate_embeddings_batch(chunks)

    chunks_indexed = vector_service.store_chunks(
        filename=file.filename,
        uploaded_by=uploaded_by,
        chunks=chunks,
        embeddings=embeddings,
    )

    return {
        "status": "success",
        "filename": file.filename,
        "chunks_indexed": chunks_indexed,
    }
