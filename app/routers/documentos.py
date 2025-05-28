from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import StreamingResponse
import io
from datetime import datetime

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/documentos", tags=["documentos"])

@router.post(
    "/upload",
    response_model=schemas.DocumentoOut,
    summary="Enviar novo documento",
    description="Faz upload de um PDF de TCC e retorna o ID, nome do arquivo e tcc_id."
)
async def upload_documento(
    titprinc: str = Query(..., alias="titprinc"),
    ano: int = Query(..., alias="ano"),
    autor_nome_curto: str = Query(..., alias="autor_nome_curto"),
    autor_nome_completo: str = Query(..., alias="autor_nome_completo"),
    subtitu: str | None = Query(None, alias="subtitu"),
    arcurdepto: str | None = Query(None, alias="arcurdepto"),
    dtdefesa: datetime | None = Query(None, alias="dtdefesa"),
    nomorienta: str | None = Query(None, alias="nomorienta"),
    grintruc: str | None = Query(None, alias="grintruc"),
    contpass: int | None = Query(None, alias="contpass"),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # Lê bytes do PDF
    content = await file.read()

    # Monta o schema de entrada com campos da requisição
    doc_in = schemas.DocumentoCreate(
        titprinc=titprinc,
        subtitu=subtitu,
        ano=ano,
        arcurdepto=arcurdepto,
        dtdefesa=dtdefesa,
        nomorienta=nomorienta,
        grintruc=grintruc,
        contpass=contpass,
        autor_nome_curto=autor_nome_curto,
        autor_nome_completo=autor_nome_completo,
    )

    # Chamada corrigida: passa db, content e doc_in
    created = await crud.create_documento(db, content, doc_in)

    return schemas.DocumentoOut(
        id=created.id,
        filename=file.filename,
        tcc_id=created.id
    )

@router.get(
    "/",
    response_model=list[schemas.DocumentoResponse],
    summary="Listar documentos",
    description="Retorna todos os documentos, ordenados do mais recente ao mais antigo."
)
async def list_documentos(
    skip: int = Query(0),
    limit: int = Query(10),
    db: AsyncSession = Depends(get_db)
):
    return await crud.list_documentos(db, skip, limit)

@router.get(
    "/recentes",
    response_model=list[schemas.DocumentoResponse],
    summary="Listar documentos recentes",
    description="Retorna os documentos mais recentes, limitado pelo parâmetro `limit`."
)
async def recentes(
    limit: int = Query(10),
    db: AsyncSession = Depends(get_db)
):
    return await crud.list_recent(db, limit)

@router.get(
    "/buscar",
    response_model=list[schemas.DocumentoResponse],
    summary="Buscar documentos",
    description="Busca documentos por quaisquer campos informados e retorna lista ordenada do mais recente ao mais antigo."
)
async def buscar(
    titprinc: str | None = Query(None, alias="titprinc"),
    subtitu: str | None = Query(None, alias="subtitu"),
    ano: int | None = Query(None, alias="ano"),
    arcurdepto: str | None = Query(None, alias="arcurdepto"),
    dtdefesa: datetime | None = Query(None, alias="dtdefesa"),
    nomorienta: str | None = Query(None, alias="nomorienta"),
    grintruc: str | None = Query(None, alias="grintruc"),
    contpass: int | None = Query(None, alias="contpass"),
    autor_nome_curto: str | None = Query(None, alias="autor_nome_curto"),
    autor_nome_completo: str | None = Query(None, alias="autor_nome_completo"),
    skip: int = Query(0),
    limit: int = Query(10),
    db: AsyncSession = Depends(get_db)
):
    return await crud.search_documentos(
        db, titprinc, subtitu, ano, arcurdepto, dtdefesa,
        nomorienta, grintruc, contpass,
        autor_nome_curto, autor_nome_completo,
        skip, limit
    )

@router.get(
    "/{documento_id}",
    response_model=schemas.DocumentoResponse,
    summary="Obter documento por ID",
    description="Retorna os metadados de um documento específico através do seu ID."
)
async def get_doc(documento_id: int, db: AsyncSession = Depends(get_db)):
    doc = await crud.get_documento(db, documento_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    return doc

@router.get(
    "/{documento_id}/download",
    summary="Download do documento",
    description="Faz download do arquivo PDF do TCC."
)
async def download_documento(documento_id: int, db: AsyncSession = Depends(get_db)):
    doc = await crud.get_documento(db, documento_id)
    if not doc or not doc.arquivo_tcc:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    return StreamingResponse(
        io.BytesIO(doc.arquivo_tcc),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=\"tcc_{documento_id}.pdf\""}
    )

@router.put(
    "/{documento_id}",
    response_model=schemas.DocumentoResponse,
    summary="Atualizar documento",
    description="Atualiza os metadados de um documento existente."
)
async def update_documento(
    documento_id: int,
    doc_in: schemas.DocumentoCreate,
    db: AsyncSession = Depends(get_db)
):
    updated = await crud.update_documento(db, documento_id, doc_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    return updated

@router.delete(
    "/{documento_id}",
    response_model=schemas.DocumentoResponse,
    summary="Excluir documento",
    description="Remove permanentemente um documento pelo seu ID."
)
async def delete_documento(documento_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_documento(db, documento_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    return deleted
