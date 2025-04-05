"""
Débogage du service d'images
"""
import json
from utils.image_service import enrich_recommendations_with_images

# Copier les données exactes de sortie pour les tester directement
test_data = [
  {
    "type": "bar",
    "nom": "Le Baron Rouge",
    "adresse": "1 Rue Théophile Roussel, 75012 Paris",
    "quartier": "Aligre",
    "points_positifs": [
      "Excellente sélection de vins",
      "Ambiance conviviale et authentique",
      "Prix abordables",
      "Terrasse agréable"
    ],
    "points_negatifs": [
      "Peut être bondé en fin de semaine",
      "Service parfois lent lors des heures de pointe"
    ]
  },
  {
    "type": "bar",
    "nom": "Le Syndicat",
    "adresse": "51 Rue du Faubourg Saint-Denis, 75010 Paris",
    "quartier": "Strasbourg - Saint-Denis",
    "points_positifs": [
      "Cocktails créatifs et bien exécutés",
      "Ambiance speakeasy chic",
      "Personnel accueillant et compétent",
      "Décoration rétro et élégante"
    ],
    "points_negatifs": [
      "Prix des cocktails assez élevés",
      "Réservation recommandée pour éviter l'attente"
    ]
  }
]

# Avant enrichissement
print("DONNÉES AVANT:")
print(json.dumps(test_data, indent=2))

# Enrichir avec des images
print("\nENRICHISSEMENT EN COURS...")
enriched_data = enrich_recommendations_with_images(test_data)

# Après enrichissement
print("\nDONNÉES APRÈS:")
print(json.dumps(enriched_data, indent=2))

# Vérifier explicitement la présence des URLs
print("\nVÉRIFICATION DES URLs:")
for i, item in enumerate(enriched_data):
    print(f"{i+1}. {item['nom']} - URL présente: {'url_image' in item}")
    if 'url_image' in item:
        print(f"   URL: {item['url_image']}")