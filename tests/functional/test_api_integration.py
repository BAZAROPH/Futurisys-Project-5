import pytest
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Ajout du chemin parent pour retrouver main.py et src
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from main import app
from src.database.models import Base, Interaction
from src.database.session import get_db
from sqlalchemy.pool import StaticPool 


#Configuration de la base de données test avec sqlite 

#Utilisation d'une base de données temporaire pour isoler les tests de la prod
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool 
)
TestingSessionLocal  = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Fonction de substitution override (utiliser sqlite au lieu de postgresql)
def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


#Appliquer la substitution
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)



#fixtures (configuration et nettoyage)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Crée les tables dans la base de données de test au début du module."""

    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def clean_database(setup_database):
    """Nettoie la table ml_interactions avant chaque test individuel"""
    db = TestingSessionLocal()

    db.query(Interaction).delete()
    db.commit()
    db.close()


#Données de Test (Identiques au schéma) ---
TEST_DATA = {
    "age": 30,
    "revenu_mensuel": 12000.0,
    "annee_experience_totale": 10,
    "annees_dans_l_entreprise": 8,
    "annees_dans_le_poste_actuel": 2,
    "satisfaction_employee_environnement": 3,
    "note_evaluation_precedente": 3,
    "niveau_hierarchique_poste": 1,
    "satisfaction_employee_nature_travail": 4,
    "satisfaction_employee_equilibre_pro_perso": 3,
    "nombre_participation_pee": 1,
    "nb_formations_suivies": 2,
    "distance_domicile_travail": 5,
    "annees_depuis_la_derniere_promotion": 1,
    "annes_sous_responsable_actuel": 1,
    "periode_stagnation": 0.5,
    "statut_marital": "Célibataire",
    "departement": "Commercial",
    "poste": "Cadre Commercial",
    "domaine_etude": "Infra & Cloud",
    "frequence_deplacement": "Frequent",
    "heure_supplementaires": "Oui"
}

#lES tests fonctionnels

def test_api_health_check():
    """Vérifie que l'API est en ligne"""
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_endpoint_success_and_logging():
    """
        Fonction qui faitles tests critique : 
            1. Envoie une requête POST valide à /predict.
            2. Vérifie le statut 200 et la réponse JSON.
            3. Vérifie qu'une ligne a été insérée dans la BDD de test (Traçabilité).
    """
    #1/Requête API
    response = client.post("/predict", json=TEST_DATA)
    assert response.status_code == 200

    data = response.json()
    assert "prediction_class" in data
    assert "probability_churn" in data

    #2/ Vérifications base de données
    db = TestingSessionLocal()
    logs = db.query(Interaction).all()

    #Nous devons avoir une seule intéraction enregistrée
    assert len(logs) == 1
    #Vérifier que les données correspondent
    assert logs[0].prediction_class == data["prediction_class"]
    assert logs[0].raw_input_json is not None

    db.close()

def test_predict_endpoint_validation_error():
    """Vérifier que l'API rejette les données incomplètes (Erreur 422)."""
    data_invalide = TEST_DATA.copy()
    del data_invalide["age"]

    response = client.post("/predict", json=data_invalide)
    assert response.status_code == 422
