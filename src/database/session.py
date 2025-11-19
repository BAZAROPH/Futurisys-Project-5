#Gestion de la connexion entre FastAPI et la base de données

from sqlalchemy.orm import sessionmaker
from src.database.create_db import engine
from sqlalchemy.orm import Session

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
        Fonction qui fournit une session de base de données thread-safe
    """
    db: Session = SessionLocal()

    try:
        yield db
    finally:
        db.close()
    