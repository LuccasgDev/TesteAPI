from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import documentos, users

app = FastAPI(
    title="API de Gerenciamento de TCCs",
    description="API em Português para upload, listagem, busca e download de documentos acadêmicos (TCCs).",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configuração de CORS liberando tudo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # permite qualquer domínio
    allow_credentials=True,
    allow_methods=["*"],       # permite todos os métodos HTTP
    allow_headers=["*"],       # permite todos os cabeçalhos
)

@app.get("/", summary="Rota raiz")
async def root():
    return {"message": "API de Gerenciamento de TCCs rodando!"}

app.include_router(documentos.router)
app.include_router(users.router)
