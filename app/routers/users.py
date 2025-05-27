from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.post(
    "/",
    response_model=schemas.UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo usuário"
)
async def create_usuario(
    usuario_in: schemas.UsuarioCreate,
    db: AsyncSession = Depends(get_db)
):
    # verifica duplicidade de e-mail
    existing = await crud.get_usuario_por_email(db, usuario_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    user = await crud.create_usuario(db, usuario_in)
    return user


@router.get(
    "/",
    response_model=list[schemas.UsuarioResponse],
    summary="Listar usuários"
)
async def list_usuarios(
    skip: int = 0, limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await crud.list_usuarios(db, skip, limit)


@router.get(
    "/{usuario_id}",
    response_model=schemas.UsuarioResponse,
    summary="Obter usuário por ID"
)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_usuario(db, usuario_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@router.put(
    "/{usuario_id}",
    response_model=schemas.UsuarioResponse,
    summary="Atualizar usuário"
)
async def update_usuario(
    usuario_id: int,
    usuario_in: schemas.UsuarioUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated = await crud.update_usuario(db, usuario_id, usuario_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return updated


@router.delete(
    "/{usuario_id}",
    response_model=schemas.UsuarioResponse,
    summary="Excluir usuário"
)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_usuario(db, usuario_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return deleted
