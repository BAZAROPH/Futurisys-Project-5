#!/bin/bash
# Script start.sh (À valider dans le dépôt actuel)

# Exécuter Gunicorn pour lancer l'application main:app
# Bind sur 0.0.0.0 pour écouter toutes les interfaces
# Port 7860 est le port standard attendu par Hugging Face Spaces
exec gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:7860