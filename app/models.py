from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Documento(Base):
    __tablename__ = 'documentos'
    id                  = Column(Integer, primary_key=True, index=True)
    titulo_principal    = Column('titulo_principal', String, nullable=False)
    subtitulo           = Column('subtitulo', String, nullable=True)
    ano                 = Column('ano', Integer, nullable=False)
    departamento        = Column('departamento', String, nullable=True)
    data_defesa         = Column('data_defesa', DateTime(timezone=True), nullable=True)
    orientador          = Column('orientador', String, nullable=True)
    grupo_instrucao     = Column('grupo_instrucao', String, nullable=True)
    arquivo_tcc         = Column('arquivo_tcc', LargeBinary, nullable=False)
    contagem_passagens  = Column('contagem_passagens', Integer, nullable=True)
    published_at        = Column('published_at', DateTime(timezone=True), default=datetime.utcnow)
    status              = Column('status', String, nullable=True)
    autor_nome_curto    = Column('autor_nome_curto', String, nullable=False, index=True)
    autor_nome_completo = Column('autor_nome_completo', String, nullable=False)

class Usuario(Base):
    __tablename__ = 'usuarios'
    id          = Column(Integer, primary_key=True, index=True)
    nome        = Column('nome', String, nullable=False)
    email       = Column('email', String, unique=True, nullable=False, index=True)
    senha_hash  = Column('senha_hash', String, nullable=False)
    tipo        = Column('tipo', String, nullable=False, default='user')
    datacad     = Column('datacad', DateTime(timezone=True), default=datetime.utcnow)
