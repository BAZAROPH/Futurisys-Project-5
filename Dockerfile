FROM python:3.10

# Création du dossier de l'app
WORKDIR /code

# Installation des dépendances
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code
COPY . /code/

# Exposer le port utilisé par Hugging Face (7860)
EXPOSE 7860

# Lancement de l'API FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
