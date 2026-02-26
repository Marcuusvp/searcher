# RAG Backend

Backend para consulta inteligente de documentos internos utilizando RAG (Retrieval-Augmented Generation).

## Visão Geral

Sistema onde membros do time fazem upload de PDFs com processos documentados, e qualquer colega pode consultar esses processos em linguagem natural via interface de chat.

## Stack Tecnológica

| Camada | Tecnologia |
|--------|------------|
| Backend | FastAPI (Python) |
| Banco de Dados + Vetorial | Supabase (PostgreSQL + pgvector) |
| LLM + Embeddings | GitHub Models (gpt-4o-mini + text-embedding-3-small) |
| Hospedagem | Render (Free tier) |

## Pré-requisitos

1. **Supabase**: Projeto criado com extensão pgvector
2. **GitHub**: Token de acesso ao Models
3. **Python 3.11+**

## Configuração

### 1. Clone o repositório

```bash
git clone <repo-url>
cd rag-backend
```

### 2. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e preencha com suas chaves:

```env
GITHUB_TOKEN=seu_token_github
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_chave_supabase
CORS_ORIGINS=*
```

### 3. Configure o Supabase

Execute os comandos SQL no editor do Supabase:

```sql
create extension if not exists vector;

create table document_chunks (
  id uuid primary key default gen_random_uuid(),
  filename text not null,
  uploaded_by text,
  content text not null,
  embedding vector(1536),
  created_at timestamp default now()
);

create or replace function match_chunks(
  query_embedding vector(1536),
  match_count int default 5
)
returns table (
  id uuid,
  filename text,
  content text,
  similarity float
)
language sql stable
as $$
  select
    id,
    filename,
    content,
    1 - (embedding <=> query_embedding) as similarity
  from document_chunks
  order by embedding <=> query_embedding
  limit match_count;
$$;
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Execute localmente

```bash
python -m uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`

Documentação interativa: `http://localhost:8000/docs`

## Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/health` | Health check |
| POST | `/upload` | Upload de PDF |
| POST | `/query` | Consulta em linguagem natural |
| GET | `/documents` | Listar documentos indexados |

Consulte `API.md` para detalhes completos.

## Deploy no Render

1. Crie um repositório GitHub e faça push do código
2. Acesse render.com e crie uma conta
3. **New → Web Service** → conecte ao repositório
4. Configure:
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Adicione as variáveis de ambiente no painel do Render
6. O Render fará o deploy e fornecerá uma URL pública

## Limitações do Free Tier

| Serviço | Limitação |
|---------|-----------|
| Render | App "dorme" após 15 min de inatividade |
| Supabase | 500MB banco, 1GB storage |
| GitHub Models | Rate limits para uso interno |

## Estrutura do Projeto

```
rag-backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── routers/
│   │   ├── upload.py
│   │   └── query.py
│   └── services/
│       ├── pdf_service.py
│       ├── embedding_service.py
│       ├── vector_service.py
│       └── llm_service.py
├── .env.example
├── .gitignore
├── requirements.txt
├── API.md
└── README.md
```

## Licença

MIT
