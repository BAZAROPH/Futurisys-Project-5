# Exemple de structure du Dockerfile (à valider)
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers essentiels
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'application, les scripts et les artefacts ML
COPY . /app/
# Assurez-vous que les fichiers .joblib sont copiés.

# Rendre le script de démarrage exécutable
RUN chmod +x start.sh

# Définir le port (HF utilise 7860)
EXPOSE 7860 

# Point d'entrée (utilise start.sh)
CMD ["./start.sh"]