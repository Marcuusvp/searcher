from openai import OpenAI
from app.config import GITHUB_TOKEN, EMBEDDING_MODEL, GITHUB_API_BASE

client = OpenAI(base_url=GITHUB_API_BASE, api_key=GITHUB_TOKEN)


def generate_embedding(text: str) -> list[float]:
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


def generate_embeddings_batch(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]
