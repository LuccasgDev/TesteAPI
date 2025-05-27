from fastapi import FastAPI
from .routers import documentos, users

app = FastAPI(
    title="API de Gerenciamento de TCCs",
    description="API em Português para upload, listagem, busca e download de documentos acadêmicos (TCCs).",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Rota raiz para verificação de saúde
@app.get("/", summary="Rota raiz")
async def root():
    return {"message": "API de Gerenciamento de TCCs rodando!"}

# Incluindo roteadores
app.include_router(documentos.router)
app.include_router(users.router)
