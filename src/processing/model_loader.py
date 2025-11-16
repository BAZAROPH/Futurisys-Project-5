# Ce fichier lie le préprocesseur au classifieur
import joblib
import os
import numpy as np
from src.processing.data_prep import prepare_data_for_prediction

#Charger le classifieur
CLASSIFIER_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'classifier.joblib')


def load_classifier():
    """
        Fonction permettant de charger le classifieur optimisé

        ----- return
        classifier: un modèle optimisé de classfication
    """

    try:
        classifier = joblib.load(CLASSIFIER_PATH)
        return classifier
    except FileNotFoundError:
        return None
    

CLASSIFIER = load_classifier()
OPTIMAL_THRESHOLD = 0.5701

#Fonction de prédiction finale
def get_prediction(raw_data: dict) -> dict:
    """
        Fonction permettant de faire une prédiction
        Prend les données brut, les prépare, puis appelle la prédiction

        ----- params
        raw_data: Dict
        les données brut d'un employé

        ----- return
        Un dictionnaire avec la classe prédite et la probabilité de démission
    """
    if CLASSIFIER is None:
        return {
            "error": "Classifier is not available (Check src/models)"
        }
    
    try:
        #Prétraitement
        X_processed = prepare_data_for_prediction(raw_data)

        #Prédiction et Probabilité
        probabilities = CLASSIFIER.predict_proba(X_processed)[0]
        prob_of_churn = probabilities[1]

        #Choix de la classe en fonction de la probabilité et le seuil optimal
        if prob_of_churn >= OPTIMAL_THRESHOLD:
            predicted_class = 1
        else:
            predicted_class = 0

        #La classe 1 est la démission, nous renvoyons sa probabilité
        prob_of_churn = float(probabilities[1])

        return {
            "prediction_class": predicted_class,
            "probability_churn": prob_of_churn
        }
    
    except Exception as e:
        return {
            "error": f"Prediction failed during processing: {str(e)}" 
        }