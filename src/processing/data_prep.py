#CE fichier applique les transformations dans le bon ordre.

import pandas as pd
import joblib
import os
from typing import Dict, Any

##1 Chargement des artefacts
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..',  'models')

ASSETS = {}

try:
    #Transformateurs
    ASSETS["scaler"] = joblib.load(os.path.join(MODEL_DIR, 'scaler.joblib'))
    ASSETS["target_encoder"] = joblib.load(os.path.join(MODEL_DIR, "target_encoder.joblib"))
    ASSETS["le_heure_sup"] = joblib.load(os.path.join(MODEL_DIR, "label_encoder_heure_sup.joblib"))

    #Liste des colonnes
    ASSETS['NUM_FEATS'] = joblib.load(os.path.join(MODEL_DIR, "numeric_features.joblib"))
    ASSETS["BIN_FEATS"] = joblib.load(os.path.join(MODEL_DIR, "binary_category.joblib"))
    ASSETS["NOM_FEATS"] = joblib.load(os.path.join(MODEL_DIR, "nominal_category.joblib"))
except FileNotFoundError as e:
    raise RuntimeError(f"Erreur de chargement d'un artefact ML essentiel: {e}")


#2 Fonction de prétraitement
def prepare_data_for_prediction(raw_data: Dict[str, Any]) -> pd.DataFrame:
    """
        Fonction qui permet d'appliquer la mise à l'échelle à une seule entrée utilisateur
    """

    #Créer d'un dataframe à partir de l'entrée utilisateur
    df = pd.DataFrame([raw_data])

    #ÉTAPES D'ENCODAGE 
    #1/ Encodage binaire (Label Enconding): heure_supplementaires
    for col in ASSETS["BIN_FEATS"]:
        df[col] = ASSETS["le_heure_sup"].transform(df[col].values)
    


    #2/ Target Encoding 
    df_nominal_encoded = ASSETS["target_encoder"].transform(df[ASSETS['NOM_FEATS']])
   
    #Remplacer les colonnes nominales par leur version encodée
    df.drop(columns=ASSETS["NOM_FEATS"], inplace=True)
    df = pd.concat([df, df_nominal_encoded], axis=1)



    # --- ÉTAPE DE SCALING (FAITE EN DERNIER) ---
    #Faire le scaling (StandardScaler)
    df[ASSETS["NUM_FEATS"]] = ASSETS["scaler"].transform(df[ASSETS["NUM_FEATS"]])
    

    # --- ORDONNANCEMENT FINAL ---
    # Définir l'ordre des colonnes tel qu'elles sont entrées dans le modèle FINAL dans le Notebook.
    # L'ordre était : [NUM_FEATS] + [BIN_FEATS] + [NOM_FEATS encodées]
    final_features_order = ASSETS["NUM_FEATS"] + ASSETS["BIN_FEATS"] + ASSETS["NOM_FEATS"]

    # 6. Sélectionner le DataFrame dans l'ordre correct et le convertir
    df = df[final_features_order]
    return df