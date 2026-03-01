from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

if settings.neon and settings.neon.strip():
    # Fix the driver name: replace 'postgres://' or 'postgresql://' with '+psycopg'
    url = settings.neon.replace("postgres://", "postgresql+psycopg://", 1)
    if "postgresql+psycopg://" not in url:
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    
    # Cloud providers like Neon require SSL
    if "sslmode" not in url:
        sep = "&" if "?" in url else "?"
        url += f"{sep}sslmode=require"
        
    SQLALCHEMY_DATABASE_URL = url
else:
    # This part is already correct because you explicitly wrote +psycopg
    SQLALCHEMY_DATABASE_URL = (
        f'postgresql+psycopg://{settings.database_username}:'
        f'{settings.database_password}@{settings.database_hostname}/'
        f'{settings.database_name}'
    )
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()