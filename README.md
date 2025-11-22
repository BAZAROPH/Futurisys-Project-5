
# Projet Futurisys : Déploiement du Modèle Prédictif de Démissions

## 1. Présentation et Objectifs du Projet

L'objectif principal de ce projet réside dans l'opérationnalisation du modèle de Machine Learning développé lors du Projet 4. Ce modèle, conçu pour anticiper les risques de démission au sein de l'effectif, est désormais accessible via une API REST développée avec le framework FastAPI.

La mise en œuvre de cette solution respecte des standards rigoureux de développement logiciel afin de garantir la pérennité et la fiabilité du système :

* Performance et Efficacité : L'utilisation conjointe de FastAPI et du serveur ASGI Uvicorn assure un traitement asynchrone des requêtes, optimisant ainsi la latence et la charge serveur.

* Assurance Qualité (QA) : La stabilité du code est validée par une suite de tests automatisés exhaustive via Pytest, garantissant la non-régression et la fiabilité des fonctionnalités.

* Traçabilité et Audit : Un système de journalisation enregistre systématiquement chaque prédiction dans une base de données PostgreSQL, permettant un audit ultérieur des décisions du modèle.

* Automatisation (CI/CD) : L'intégration et le déploiement continus sont assurés par GitHub Actions, automatisant les phases de test et de livraison logicielle.

## 2. Procédures d'Installation et de Configuration (Environnement Local)

### 2.1. Prérequis Techniques

Le bon fonctionnement de l'application nécessite l'environnement suivant :

* Python 3.10 ou version ultérieure.

* Une instance de serveur **PostgreSQL** active (port par défaut : `5432`).

* Un rôle utilisateur PostgreSQL disposant des privilèges nécessaires à la création de bases de données (ex: `futurisys_user`).

### 2.2. Installation de l'Application

Veuillez suivre les étapes ci-dessous pour initialiser l'environnement de développement :

```bash
# 1. Clonage du dépôt distant
git clone [https://votre-url-de-depot.com/futurisys_ml_api.git](https://votre-url-de-depot.com/futurisys_ml_api.git)
cd futurisys_ml_api

# 2. Création et activation de l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Sous Windows : venv\Scripts\activate

# 3. Installation des dépendances (Machine Learning et Base de Données)
pip install -r requirements.txt 
```


### 2.3. Configuration de la Sécurité et de la Base de Données

La gestion des identifiants sensibles est assurée par des variables d'environnement. Veuillez configurer le fichier `.env.example` en supprimant l'extension `.example` à la racine du projet:

Configuration du fichier `.env` :

```bash
DB_USER=votre_utilisateur
DB_PASSWORD=votre_mot_de_passe_securise
DB_HOST=votre_adresse_serveur
DB_PORT=votre_port
DB_NAME=votre_base_de_donnée
```


Une fois la configuration établie, exécutez le script d'initialisation pour générer le schéma de base de données :
```bash
python -m src.database.create_db
```

### 2.4. Démarrage du Serveur API

Après la configuration de la base de données, démarrez le serveur d'application via la commande suivante :
```bash
python -m uvicorn main:app --reload --port 8000
```

L'interface de programmation est dès lors accessible à l'adresse : `http://127.0.0.1:8000` si vous êtes en local.

## 3. Guide d'Utilisation et Documentation de l'API

L'API expose un point de terminaison principal, `/predict`, lequel requiert un jeu de **22** variables caractéristiques d'un employé pour évaluer la probabilité de démission.

### 3.1. Documentation Technique (Swagger UI)

FastAPI génère automatiquement une documentation interactive conforme aux spécifications OpenAPI.
Accès à la documentation : `http://127.0.0.1:8000/docs`

Cette interface permet de consulter la structure attendue des données d'entrée (`DataInput`) ainsi que le format de la réponse (`PredictionOutput`).

### 3.2. Mécanisme de Traçabilité (Logging)

Afin de garantir la transparence et le suivi des opérations :

* Toute prédiction validée entraîne l'archivage du résultat et des données d'entrée associées dans la table `ml_interactions`.

* Cette persistance des données est cruciale pour l'audit des performances du modèle et l'analyse comportementale des requêtes.

## 4. Architecture et Assurance Qualité

### 4.1. Stratégie de Gestion de Versions (Gitflow)

Le développement suit la méthodologie **Gitflow** pour structurer le cycle de vie du logiciel :

* `main` : Branche de production, ne contenant que du code stable et validé.

* `develop` : Branche d'intégration principale pour les nouvelles fonctionnalités.

* **Tags** (`v1.0.0`, etc.) : Étiquetage rigoureux des versions publiées.

### 4.2. Pipeline d'Intégration et de Déploiement Continus (CI/CD)

Le pipeline **GitHub Actions** assure la conformité et la qualité du code :

* **Validation Automatisée** : L'exécution de la suite de tests (**Pytest**) est déclenchée systématiquement lors des modifications sur la branche `develop`. La réussite intégrale des tests constitue une condition sine qua non pour la fusion du code.

* **Déploiement Contrôlé** : Le processus de déploiement en production est restreint à la branche `main`, intervenant uniquement après validation définitive.

## 5. Justifications Techniques et Analytiques

**Choix Technologiques**

* **FastAPI** et **SQLAlchemy** : Cette pile technologique a été sélectionnée pour ses performances élevées et sa gestion robuste de la concurrence (thread-safety) lors des transactions en base de données.

* **Seuil de Décision (0.5701)** : Le seuil optimal, déterminé lors de la phase d'analyse exploratoire, a été intégré statiquement dans le module `model_loader.py`. Cette mesure vise à maximiser le rappel (Recall), assurant ainsi une détection efficace des profils à risque.

**Bénéfices pour l'Analyse de Données**

L'archivage systématique des interactions en base de données constitue un atout stratégique pour l'équipe Data. Cela permet notamment :

* Le suivi (monitoring) des performances du modèle en conditions réelles de production.

* L'analyse des distributions de données d'entrée afin de détecter d'éventuelles dérives (**Data Drift**) dans les caractéristiques des nouveaux employés.
