from supabase import create_client, Client
from app.config import SUPABASE_URL, SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE_NAME = "document_chunks"


def store_chunks(
    filename: str, uploaded_by: str, chunks: list[str], embeddings: list[list[float]]
) -> int:
    records = []
    for chunk, embedding in zip(chunks, embeddings):
        records.append(
            {
                "filename": filename,
                "uploaded_by": uploaded_by,
                "content": chunk,
                "embedding": embedding,
            }
        )

    supabase.table(TABLE_NAME).insert(records).execute()
    return len(records)


def search_similar_chunks(
    query_embedding: list[float], match_count: int = 5
) -> list[dict]:
    response = supabase.rpc(
        "match_chunks", {"query_embedding": query_embedding, "match_count": match_count}
    ).execute()
    return response.data


def get_all_documents() -> list[dict]:
    response = (
        supabase.table(TABLE_NAME).select("filename, uploaded_by, created_at").execute()
    )
    docs = []
    for item in response.data:
        if item["filename"] not in [d["filename"] for d in docs]:
            docs.append(item)
    return docs


def delete_document(filename: str) -> int:
    response = supabase.table(TABLE_NAME).delete().eq("filename", filename).execute()
    return len(response.data) if response.data else 0
