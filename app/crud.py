# app/crud.py

from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy import desc, and_
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext

from .models import Documento, Usuario
from .schemas import DocumentoCreate, UsuarioCreate, UsuarioUpdate

# contexto de hashing de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ------------------------
# CRUD de Documento
# ------------------------

async def create_documento(db: AsyncSession, content: bytes, doc_in: DocumentoCreate) -> Documento:
    new = Documento(
        titulo_principal   = doc_in.titulo_principal,
        subtitulo          = doc_in.subtitulo,
        ano                = doc_in.ano,
        departamento       = doc_in.departamento,
        data_defesa        = doc_in.data_defesa,
        orientador         = doc_in.orientador,
        grupo_instrucao    = doc_in.grupo_instrucao,
        contagem_passagens = doc_in.contagem_passagens,
        arquivo_tcc        = content,
        published_at       = datetime.utcnow(),
        autor_nome_curto   = doc_in.autor_nome_curto,
        autor_nome_completo= doc_in.autor_nome_completo,
    )
    db.add(new)
    await db.commit()
    await db.refresh(new)
    return new

async def get_documento(db: AsyncSession, documento_id: int) -> Documento | None:
    result = await db.execute(select(Documento).where(Documento.id == documento_id))
    return result.scalars().first()

async def list_documentos(db: AsyncSession, skip: int, limit: int) -> list[Documento]:
    q = select(Documento).order_by(desc(Documento.published_at)).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()

async def list_recent(db: AsyncSession, limit: int) -> list[Documento]:
    q = select(Documento).order_by(desc(Documento.published_at)).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()

async def search_documentos(
    db: AsyncSession,
    titprinc: str | None = None,
    subtitu: str | None = None,
    ano: int | None = None,
    arcurdepto: str | None = None,
    dtdefesa: datetime | None = None,
    nomorienta: str | None = None,
    grintruc: str | None = None,
    contpass: int | None = None,
    autor_nome_curto: str | None = None,
    autor_nome_completo: str | None = None,
    skip: int = 0,
    limit: int = 10
) -> list[Documento]:
    filters = []
    if titprinc:          filters.append(Documento.titulo_principal.ilike(f"%{titprinc}%"))
    if subtitu:           filters.append(Documento.subtitulo.ilike(f"%{subtitu}%"))
    if ano is not None:   filters.append(Documento.ano == ano)
    if arcurdepto:        filters.append(Documento.departamento.ilike(f"%{arcurdepto}%"))
    if dtdefesa:          filters.append(Documento.data_defesa == dtdefesa)
    if nomorienta:        filters.append(Documento.orientador.ilike(f"%{nomorienta}%"))
    if grintruc:          filters.append(Documento.grupo_instrucao.ilike(f"%{grintruc}%"))
    if contpass is not None:
                          filters.append(Documento.contagem_passagens == contpass)
    if autor_nome_curto:  filters.append(Documento.autor_nome_curto.ilike(f"%{autor_nome_curto}%"))
    if autor_nome_completo:
                          filters.append(Documento.autor_nome_completo.ilike(f"%{autor_nome_completo}%"))

    q = select(Documento)
    if filters:
        q = q.where(and_(*filters))
    q = q.order_by(desc(Documento.published_at)).offset(skip).limit(limit)

    result = await db.execute(q)
    return result.scalars().all()

async def update_documento(db: AsyncSession, documento_id: int, doc_in: DocumentoCreate) -> Documento | None:
    doc = await get_documento(db, documento_id)
    if not doc:
        return None

    # atualiza dinamicamente todos os campos do schema
    for field, value in doc_in.model_dump(by_alias=True).items():
        setattr(doc, field, value)

    await db.commit()
    await db.refresh(doc)
    return doc

async def delete_documento(db: AsyncSession, documento_id: int) -> Documento | None:
    doc = await get_documento(db, documento_id)
    if not doc:
        return None

    await db.delete(doc)
    await db.commit()
    return doc


# ------------------------
# CRUD de Usuario
# ------------------------

async def get_usuario(db: AsyncSession, usuario_id: int) -> Usuario | None:
    result = await db.execute(select(Usuario).where(Usuario.id == usuario_id))
    return result.scalars().first()

async def get_usuario_por_email(db: AsyncSession, email: str) -> Usuario | None:
    result = await db.execute(select(Usuario).where(Usuario.email == email))
    return result.scalars().first()

async def list_usuarios(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Usuario]:
    result = await db.execute(select(Usuario).offset(skip).limit(limit))
    return result.scalars().all()

async def create_usuario(db: AsyncSession, usuario_in: UsuarioCreate) -> Usuario:
    hashed_pwd = pwd_context.hash(usuario_in.senha)
    db_user = Usuario(
        nome       = usuario_in.nome,
        email      = usuario_in.email,
        senha_hash = hashed_pwd,
        tipo       = "user"
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_usuario(db: AsyncSession, usuario_id: int, usuario_in: UsuarioUpdate) -> Usuario | None:
    user = await get_usuario(db, usuario_id)
    if not user:
        return None

    for field, value in usuario_in.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user

async def delete_usuario(db: AsyncSession, usuario_id: int) -> Usuario | None:
    user = await get_usuario(db, usuario_id)
    if not user:
        return None

    await db.delete(user)
    await db.commit()
    return user
