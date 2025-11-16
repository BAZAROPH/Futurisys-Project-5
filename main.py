from fastapi import FastAPI, HTTPException
import uvicorn
from src.processing.model_loader import get_prediction
from src.processing.schemas import DataInput, PredictionOutput

#Initialisation de l'API
app = FastAPI(
    title="Futurisys ML API - Churn Prediction",
    description="API for predicting employee chrun risk based on HR and Survey data",
    version="1.0.0"
)

#Endpoint de santé
@app.get("/", tags=["Health Check"])
def home():
    """Endpoint de base pour vérifier que l'API est en cours d'exécution."""
    return {
        "status": "ok",
        "message": "ML API is running."
    }

#Endpoint de prédiction
@app.post("/predict", response_model=PredictionOutput, tags=["Prediction"])
def predict(data: DataInput):
    """
        Endpoint qui réalise une prédiction du risque de démission en utilisant les données d'entrée.
    """

    #Convertir l'objet Pydantic en dictionnaire pour le préprocesseur
    raw_data_dict = data.model_dump()

    #Appel du pipeline complet
    result = get_prediction(raw_data_dict)
    print(result)
    if "error" in result:
        #Gère les erreur de chargement ou de preprocessing
        raise HTTPException(status_code=500, detail=result["error"])
    
    #Définition du message de sortie
    message = "High churn risk (Employee predicted to leave)" if result["prediction_class"] == 1 else "Low churn risk (Employee predicted to stay)"

    #Retourner le résultat
    return PredictionOutput(
        prediction_class=result["prediction_class"],
        probability_churn=result["probability_churn"],
        message=message
    )

#Lancement de l'application (pour le test local)
if __name__ == "__main__":
    # Pour lancer: uvicorn main:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)
