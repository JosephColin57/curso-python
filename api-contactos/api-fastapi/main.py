from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from database import Contacto as ContactoDB, get_db

app = FastAPI(title='API de Contactos', version='1.0.0')

# Modelo de datos - Pydantic valida automáticamente los datos de entrada
class ContactoIn(BaseModel):
    nombre: str
    telefono: str
    email: EmailStr

class ContactoOut(ContactoIn):
    id: int
    class Config:
        from_attributes = True

# Endpoint para recibir el formulario de contacto
@app.get('/')
def inicio():
    return {'mensaje': 'API Contactos con FastAPI'}

@app.get("/contactos", response_model=list[ContactoOut])
def listar_contactos(db: Session = Depends(get_db)):
    contactos = db.query(ContactoDB).all()
    return contactos

@app.get("/contactos/{id}", response_model=ContactoOut)
def obtener_contacto(id: int, db: Session = Depends(get_db)):
    contacto = db.query(ContactoDB).filter(ContactoDB.id == id).first()
    if not contacto:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    return contacto

@app.post("/contactos", response_model=ContactoOut, status_code=201)
def crear_contacto(contacto: ContactoIn, db: Session = Depends(get_db)):
    nuevo = ContactoDB(**contacto.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.put("/contactos/{id}", response_model=ContactoOut)
def actualizar_contacto(id: int, contacto: ContactoIn, db: Session = Depends(get_db)):
    contacto_db = db.query(ContactoDB).filter(ContactoDB.id == id).first()
    if not contacto_db:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    for key, value in contacto.model_dump().items():
        setattr(contacto_db, key, value)
    db.commit()
    db.refresh(contacto_db)
    return contacto_db

@app.delete("/contactos/{id}", status_code=204)
def eliminar_contacto(id: int, db: Session = Depends(get_db)):
    contacto_db = db.query(ContactoDB).filter(ContactoDB.id == id).first()
    if not contacto_db:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    db.delete(contacto_db)
    db.commit()
    return {'Mensaje': f'Contacto {id} eliminado exitosamente'}