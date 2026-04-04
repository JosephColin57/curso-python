from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

class UsuarioDB(base):
    __tablename__ = 'usuarios'
    
    id       = Column(Integer, primary_key=True, index=True)
    email    = Column(String(120), unique=True, nullable=False)
    password = Column(String(200), nullable=False)


class ContactoDB(base):
    __tablename__ = 'contactos'
    
    id         = Column(Integer, primary_key=True, index=True)
    nombre     = Column(String(100), nullable=False)
    telefono   = Column(String(20), nullable=False)
    email      = Column(String(120), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
