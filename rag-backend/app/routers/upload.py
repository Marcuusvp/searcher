from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services import pdf_service, embedding_service, vector_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/upload", tags=["upload"])

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("")
async def upload_pdf(file: UploadFile = File(...), uploaded_by: str = Form(...)):
    logger.info(f"Starting upload: {file.filename}")

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_bytes = await file.read()

    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400, detail="File too large. Maximum size is 10MB"
        )

    logger.info(f"File size: {len(file_bytes)} bytes")

    try:
        text = pdf_service.extract_text_from_pdf(file_bytes)
        logger.info(f"Extracted text length: {len(text)} chars")
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")

    chunks = pdf_service.chunk_text(text)
    logger.info(f"Created {len(chunks)} chunks")

    try:
        embeddings = embedding_service.generate_embeddings_batch(chunks)
        logger.info(f"Generated {len(embeddings)} embeddings")
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error generating embeddings: {str(e)}"
        )

    try:
        chunks_indexed = vector_service.store_chunks(
            filename=file.filename,
            uploaded_by=uploaded_by,
            chunks=chunks,
            embeddings=embeddings,
        )
        logger.info(f"Stored {chunks_indexed} chunks")
    except Exception as e:
        logger.error(f"Error storing chunks: {e}")
        raise HTTPException(status_code=500, detail=f"Error storing chunks: {str(e)}")

    return {
        "status": "success",
        "filename": file.filename,
        "chunks_indexed": chunks_indexed,
    }
