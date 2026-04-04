from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from database import get_db
from models import UsuarioDB, ContactoDB
from auth import hash_password, verify_password, create_access_token, verify_token

app = FastAPI(title='API de Contactos', version='2.0.0')
security = HTTPBearer()

# ─── Schemas ────────────────────────────────────────────
class UsuarioIn(BaseModel):
    email: EmailStr
    password: str

class ContactoIn(BaseModel):
    nombre: str
    telefono: str
    email: EmailStr

class ContactoOut(BaseModel):
    id: int
    nombre: str
    telefono: str
    email: str
    class Config:
        from_attributes = True

# ─── Dependencia — obtener usuario actual ────────────────

def get_usuario_actual(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token inválido o expirado'
        )
    usuario = db.query(UsuarioDB).filter(
        UsuarioDB.id == int(payload['sub'])
    ).first()
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return usuario

# ─── Auth ───────────────────────────────────────────────
@app.post('/auth/registro', status_code=201)
def registro(datos: UsuarioIn, db: Session = Depends(get_db)):
    if db.query(UsuarioDB).filter(UsuarioDB.email == datos.email).first():
        raise HTTPException(status_code=400, detail='Email ya registrado')
    usuario = UsuarioDB(
        email=datos.email,
        password=hash_password(datos.password)
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return {'mensaje': 'Usuario creado', 'id': usuario.id}

@app.post('/auth/login')
def login(datos: UsuarioIn, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == datos.email).first()
    if not usuario or not verify_password(datos.password, usuario.password):
        raise HTTPException(status_code=401, detail='Credenciales inválidas')
    token = create_access_token({'sub': str(usuario.id)})
    return {'access_token': token, 'token_type': 'bearer'}

# ─── Contactos protegidos ────────────────────────────────
@app.get('/contactos', response_model=list[ContactoOut])
def listar_contactos(
    usuario: UsuarioDB = Depends(get_usuario_actual),
    db: Session = Depends(get_db)
):
    return db.query(ContactoDB).filter(
        ContactoDB.usuario_id == usuario.id
    ).all()

@app.post('/contactos', response_model=ContactoOut, status_code=201)
def crear_contacto(
    datos: ContactoIn,
    usuario: UsuarioDB = Depends(get_usuario_actual),
    db: Session = Depends(get_db)
):
    contacto = ContactoDB(**datos.model_dump(), usuario_id=usuario.id)
    db.add(contacto)
    db.commit()
    db.refresh(contacto)
    return contacto

@app.get('/contactos/{id}', response_model=ContactoOut)
def obtener_contacto(
    id: int,
    usuario: UsuarioDB = Depends(get_usuario_actual),
    db: Session = Depends(get_db)
):
    contacto = db.query(ContactoDB).filter(
        ContactoDB.id == id,
        ContactoDB.usuario_id == usuario.id
    ).first()
    if not contacto:
        raise HTTPException(status_code=404, detail='Contacto no encontrado')
    return contacto

@app.put('/contactos/{id}', response_model=ContactoOut)
def actualizar_contacto(
    id: int,
    datos: ContactoIn,
    usuario: UsuarioDB = Depends(get_usuario_actual),
    db: Session = Depends(get_db)
):
    contacto = db.query(ContactoDB).filter(
        ContactoDB.id == id,
        ContactoDB.usuario_id == usuario.id
    ).first()
    if not contacto:
        raise HTTPException(status_code=404, detail='Contacto no encontrado')
    for campo, valor in datos.model_dump().items():
        setattr(contacto, campo, valor)
    db.commit()
    db.refresh(contacto)
    return contacto

@app.delete('/contactos/{id}')
def eliminar_contacto(
    id: int,
    usuario: UsuarioDB = Depends(get_usuario_actual),
    db: Session = Depends(get_db)
):
    contacto = db.query(ContactoDB).filter(
        ContactoDB.id == id,
        ContactoDB.usuario_id == usuario.id
    ).first()
    if not contacto:
        raise HTTPException(status_code=404, detail='Contacto no encontrado')
    db.delete(contacto)
    db.commit()
    return {'mensaje': f'Contacto {id} eliminado'}