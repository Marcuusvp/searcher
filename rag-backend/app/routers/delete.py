from fastapi import APIRouter
from app.services import vector_service

router = APIRouter(prefix="/documents", tags=["documents"])


@router.delete("/{filename}")
async def delete_document(filename: str):
    deleted_count = vector_service.delete_document(filename)
    return {"status": "success", "deleted_count": deleted_count}
