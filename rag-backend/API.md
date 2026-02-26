# API RAG - Documentação de Endpoints

## Configuração Inicial

### Variáveis de Ambiente

Crie um arquivo `.env` na pasta `rag-backend/`:

```env
GITHUB_TOKEN=seu_token_github
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_chave_supabase
CORS_ORIGINS=*
```

### Instalação e Execução

```bash
cd rag-backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`

---

## Endpoints

### 1. Health Check

Verifica se a API está funcionando.

**Endpoint:** `GET /health`

**Exemplo de chamada:**

```bash
curl http://localhost:8000/health
```

**Resposta:**
```json
{
  "status": "healthy"
}
```

---

### 2. Upload de PDF

Faz upload de um PDF para processamento e indexação.

**Endpoint:** `POST /upload`

**Parâmetros (multipart/form-data):**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| file | File | Arquivo PDF |
| uploaded_by | String | Nome de quem está fazendo o upload |

**Exemplo de chamada:**

```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@exemplo.pdf" \
  -F "uploaded_by=João"
```

**Resposta de sucesso:**
```json
{
  "status": "success",
  "filename": "exemplo.pdf",
  "chunks_indexed": 14
}
```

**Possíveis erros:**
- `"Only PDF files are supported"` - O arquivo deve ser PDF

---

### 3. Consulta de Documentos

Faz uma pergunta em linguagem natural e retorna a resposta baseada nos documentos indexados.

**Endpoint:** `POST /query`

**Corpo da requisição (application/json):**

```json
{
  "question": "sua pergunta aqui"
}
```

**Exemplo de chamada:**

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "Como funciona o processo de onboarding?"}'
```

**Resposta:**
```json
{
  "answer": "O processo de onboarding consiste em...",
  "sources": ["exemplo.pdf"]
}
```

---

### 4. Listar Documentos

Lista todos os documentos que foram indexados no sistema.

**Endpoint:** `GET /documents`

**Exemplo de chamada:**

```bash
curl http://localhost:8000/documents
```

**Resposta:**
```json
{
  "documents": [
    {
      "filename": "exemplo.pdf",
      "uploaded_by": "João",
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

---

## Documentação Interativa

Acesse `http://localhost:8000/docs` no navegador para ver a documentação Swagger/OpenAPI interativa, onde você pode testar todos os endpoints diretamente.

---

## Fluxo de Uso

1. **Faça upload de PDFs** usando o endpoint `/upload`
2. **Consulte os documentos** usando o endpoint `/query`
3. **Liste os documentos** indexados usando `/documents`

---

## Configuração do Supabase (Pré-requisitos)

Antes de usar a API, certifique-se de ter:

1. **Projeto Supabase criado** em supabase.com
2. **Extensão pgvector** habilitada:
   ```sql
   create extension if not exists vector;
   ```
3. **Tabela criada**:
   ```sql
   create table document_chunks (
     id uuid primary key default gen_random_uuid(),
     filename text not null,
     uploaded_by text,
     content text not null,
     embedding vector(1536),
     created_at timestamp default now()
   );
   ```
4. **Função de busca**:
   ```sql
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
