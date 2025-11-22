#fichier pour la création des modèles de base de données

from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, UTC

Base = declarative_base()

class Interaction(Base):
    """
        Modèle qui enregistre la traçabilité des prédicions machine learning
    """

    __tablename__ = "ml_interactions"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now(UTC))

    #Outputs du modèle
    prediction_class = Column(Integer, nullable=False)
    probability_churn = Column(Float, nullable=False)

    #Inputs pour l'analyse(stockage des entrées complètes pour l'analyse future)
    raw_input_json = Column(String)
