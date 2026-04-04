from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from bcrypt import hashpw, gensalt, checkpw
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'clave-secreta-muy-larga-2024-fastapi')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def hash_password(password: str) -> str:
    return hashpw(
        password.encode('utf-8'),
        gensalt()
    ).decode('utf-8')


def verify_password(password: str, hash: str) -> bool:
    return checkpw(
        password.encode('utf-8'),
        hash.encode('utf-8')
    )

def create_access_token(data: dict) -> str:
    datos = data.copy()
    expira = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos.update({"exp": expira})
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None