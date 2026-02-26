import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"
GITHUB_API_BASE = "https://models.inference.ai.azure.com"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
