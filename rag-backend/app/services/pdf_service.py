import pdfplumber
from io import BytesIO
from app.config import CHUNK_SIZE, CHUNK_OVERLAP


def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def chunk_text(text: str) -> list[str]:
    tokens = text.split()
    chunks = []

    for i in range(0, len(tokens), CHUNK_SIZE - CHUNK_OVERLAP):
        chunk = " ".join(tokens[i : i + CHUNK_SIZE])
        if chunk:
            chunks.append(chunk)

    return chunks
