from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL (using SQLite for simplicity)
SQLALCHEMY_DATABASE_URL = "sqlite:///./contactos.db"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Create a base class for our models
Base = declarative_base()

# Define the Contacto model
class Contacto(Base):
    __tablename__ = "contactos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    telefono = Column(String, index=True)
    email = Column(String, unique=True, index=True)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
