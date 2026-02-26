from openai import OpenAI
from app.config import GITHUB_TOKEN, LLM_MODEL, GITHUB_API_BASE

client = OpenAI(base_url=GITHUB_API_BASE, api_key=GITHUB_TOKEN)


def generate_answer(question: str, context_chunks: list[dict]) -> tuple[str, list[str]]:
    context = "\n\n".join([chunk["content"] for chunk in context_chunks])
    sources = list(set(chunk["filename"] for chunk in context_chunks))

    prompt = f"""Baseie-se exclusivamente no contexto abaixo para responder a pergunta. 
Se a resposta não estiver no contexto, diga que não possui informação suficiente.

Contexto:
{context}

Pergunta: {question}

Resposta:"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Você é um assistente que responde perguntas sobre documentos internos.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    answer = response.choices[0].message.content
    return answer, sources
