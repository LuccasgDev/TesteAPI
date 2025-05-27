from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime

# usado para criar/atualizar Documento
class DocumentoCreate(BaseModel):
    titulo_principal: str               = Field(..., alias="titprinc")
    subtitulo: Optional[str]            = Field(None,  alias="subtitu")
    ano: int                            = Field(..., alias="ano")
    departamento: Optional[str]         = Field(None,  alias="arcurdepto")
    data_defesa: Optional[datetime]     = Field(None,  alias="dtdefesa")
    orientador: Optional[str]           = Field(None,  alias="nomorienta")
    grupo_instrucao: Optional[str]      = Field(None,  alias="grintruc")
    contagem_passagens: Optional[int]   = Field(None,  alias="contpass")
    autor_nome_curto: str               = Field(..., alias="autor_nome_curto")
    autor_nome_completo: str            = Field(..., alias="autor_nome_completo")

    class Config:
        allow_population_by_field_name = True


# usado para listar, buscar, obter por ID
class DocumentoResponse(BaseModel):
    id: int
    titulo_principal: str
    subtitulo: Optional[str]            = None
    ano: int
    departamento: Optional[str]         = None
    data_defesa: Optional[datetime]     = None
    orientador: Optional[str]           = None
    grupo_instrucao: Optional[str]      = None
    contagem_passagens: Optional[int]   = None
    published_at: datetime
    status: Optional[str]               = None
    autor_nome_curto: str
    autor_nome_completo: str

    class Config:
        from_attributes = True


# usado apenas na rota de upload para retorno
class DocumentoOut(BaseModel):
    id: int
    filename: str
    tcc_id: int

    class Config:
        from_attributes = True


# --- Schemas para Usuario ---

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=6)

    @validator('senha')
    def senha_min_length(cls, v):
        if len(v) < 6:
            raise ValueError('Senha muito curta')
        return v


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    tipo: Optional[str] = None


class UsuarioResponse(UsuarioBase):
    id: int
    tipo: str
    datacad: datetime

    class Config:
        orm_mode = True


class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str
