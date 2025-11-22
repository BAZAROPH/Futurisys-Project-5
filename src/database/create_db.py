#Fichier pour la création de la base de données

from sqlalchemy import create_engine
from src.database.models import Base
import os
from dotenv import load_dotenv

#Chagrer mes variables du .env
load_dotenv()

#Configuration de la connexion base de données
DB_USER = os.getenv("DB_USER", "user_default")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password_default")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "db_default")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)

def create_database_tables():
    """
        Fonction qui créée toutes les tables définies via les modèles
    """

    try:
        Base.metadata.create_all(bind=engine)
        print("Base de données et tables créées avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création de la base de données: {e}")


if __name__ == "__main__":
    create_database_tables()