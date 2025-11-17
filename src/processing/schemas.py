from pydantic import BaseModel
from typing import Optional

#Pydantic définit les données que l'API attend en entrée
#Le schéma inclut toutes les features d'entrée nécessaires pour la prédiction
class DataInput(BaseModel):
    #Variabales Numériques (scaling requis)
    age: int
    revenu_mensuel: float
    annee_experience_totale: int
    annees_dans_l_entreprise: int
    annees_dans_le_poste_actuel: int
    satisfaction_employee_environnement: int
    note_evaluation_precedente: int
    niveau_hierarchique_poste: int
    satisfaction_employee_nature_travail: int
    satisfaction_employee_equilibre_pro_perso: int
    nombre_participation_pee: int
    nb_formations_suivies: int
    distance_domicile_travail: int
    annees_depuis_la_derniere_promotion: int
    annes_sous_responsable_actuel: int
    periode_stagnation: float

    #Variables Catégorielles (encodage requis)
    statut_marital: str
    departement: str
    poste: str
    domaine_etude: str
    frequence_deplacement: str

    #Variable Binaire (Label Encoding requis)
    heure_supplementaires: str # "Oui" ou "Non"


class Config:
    schema_extra = {
        "example": {
            "age": 30,
            "revenu_mensuel": 4500.0,
            "annee_experience_totale": 5,
            "annees_dans_l_entreprise": 3,
            "annees_dans_le_poste_actuel": 2,
            "satisfaction_employee_environnement": 3,
            "note_evaluation_precedente": 3,
            "niveau_hierarchique_poste": 1,
            "satisfaction_employee_nature_travail": 4,
            "satisfaction_employee_equilibre_pro_perso": 3,
            "nombre_participation_pee": 1,
            "nb_formations_suivies": 2,
            "distance_domicile_travail": 15,
            "annees_depuis_la_derniere_promotion": 1,
            "annes_sous_responsable_actuel": 1,
            "periode_stagnation": 1.5, # Exemple de ratio (à calculer avant l'appel)
            "statut_marital": "Marié(e)",
            "departement": "Consulting",
            "poste": "Consultant",
            "domaine_etude": "Infra & Cloud",
            "frequence_deplacement": "Occasionnel",
            "heure_supplementaires": "Non"
        }
    }

# Schéma de sortie
class PredictionOutput(BaseModel):
    prediction_class: int #1 pour démission et 0 pour non démission
    probability_churn: float
    message: str