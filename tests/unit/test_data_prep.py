#Fichier qui gère les tests unitaires pour la préparation des données
import pytest
import sys
import os
import pandas as pd

# Ajout du chemin parent pour retrouver le package src
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

#Modules de production testé
from src.processing.data_prep import ASSETS, prepare_data_for_prediction
from src.processing.model_loader import load_classifier, get_prediction

#___ Jeu de donné fictif
TEST_INPUT_RAW = {
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

@pytest.fixture(scope="module")
def processed_data():
    """Fixture qui exécute le prétraitement prepare_data_for_prediction une seule fois"""
    return prepare_data_for_prediction(TEST_INPUT_RAW)

#A     Vérifier la conformité du chargement
def test_artefacts_loading_success():
    """
        Fonction qui vérifie que les transformateurs et les listes de features sont bien chargés
    """
    assert ASSETS is not None
    assert 'scaler' in ASSETS

    #Vérifier qu'on a 22 colonnes
    assert len(ASSETS["NUM_FEATS"] + ASSETS["BIN_FEATS"] + ASSETS["NOM_FEATS"]) == 22

def test_classifier_loading_success():
    """Vérifie que le modèle de Régression Logistique est chargé en mémoire."""
    classifier = load_classifier()
    assert classifier is not None


#B.     Tests de la Logique machine learning

def test_prepare_data_output_shape(processed_data):
    """
        Fonction qui vérifie que le pipeline retourne la forme et le type attendus 
        1 ligne
        22 colonnes
        DataFrame
    """
    assert processed_data.shape == (1, 22), f"Forme attendue (1, 22), reçue {processed_data.shape}"
    assert isinstance(processed_data, pd.DataFrame), "Le modèle final attend un DataFrame."



def test_prepare_data_scaling_applied(processed_data):
    """
        Fonction qui vérifie que le StandarScaler a été appliqué (la valeur n'est plus la valeur brute)
    """

    #trouver l'index de la colonne age dans la liste final
    final_orderer_list = ASSETS["NUM_FEATS"] + ASSETS["BIN_FEATS"] + ASSETS["NOM_FEATS"]
    age_index = final_orderer_list.index('age')
    age_transformed_value = processed_data.iloc[0, age_index]

    #La valeur valeur trasnformée ne doit pas correspondre à la valeur initiale
    assert age_transformed_value != TEST_INPUT_RAW["age"], "Le scaling n'a pas été appliqué."



def test_prediction_returns_valid_result():
    """
        Fonction qui vérifie que la fonction get_predict retourne bien un dictionnaire avec une classe et une probabilité qui sont valides
    """

    result = get_prediction(TEST_INPUT_RAW)

    assert "error" not in result
    assert isinstance(result["prediction_class"], int)
    assert result["prediction_class"] in [0, 1]
    assert 0.0 <= result["probability_churn"] <= 1.0
