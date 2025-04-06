"""
Configuration de l'application
"""
import os
from dotenv import load_dotenv

# Charger les variables d'environnement si un fichier .env existe
try:
    load_dotenv()
except:
    pass  # Si python-dotenv n'est pas installé, on ignore

# Configuration Mistral
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY", "DnCAyOg2sUZx3jIwSASA9GWLByW1sanp")
MISTRAL_MODEL = os.environ.get("MISTRAL_MODEL", "mistral-large-latest")

# Configuration de l'application
DEFAULT_OUTPUT_FORMAT = "json"
DEFAULT_LOCATION = "Paris"
TEMPERATURE = 0.7
MAX_TOKENS = 2000