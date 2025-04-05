"""
Module pour récupérer des images via Unsplash
"""
from urllib.parse import quote_plus
import time
import requests

def get_unsplash_image(search_term):
    """
    Récupère une image Unsplash aléatoire
    
    Args:
        search_term (str): Le terme de recherche
        
    Returns:
        str: URL de l'image ou image par défaut
    """
    print(f"Recherche d'image pour: '{search_term}'")
    
    try:
        encoded_term = quote_plus(search_term)
        url = f"https://source.unsplash.com/random/?{encoded_term}"
        
        # Utiliser une requête HEAD pour ne pas télécharger l'image
        response = requests.head(url, allow_redirects=True)
        
        # Vérifier si la requête a réussi
        if response.status_code == 200:
            final_url = response.url
            print(f"Image trouvée: {final_url}")
            return final_url
            
    except Exception as e:
        print(f"Erreur: {e}")
    
    # Image par défaut si échec
    default_url = "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad"
    print(f"Utilisation image par défaut: {default_url}")
    return default_url

def enrich_recommendations_with_images(recommendations, location="Paris"):
    """
    Ajoute des URLs d'images aux recommandations
    
    Args:
        recommendations (list): Liste des recommandations
        location (str): Ville pour les recommandations
        
    Returns:
        list: Recommandations enrichies avec des URLs d'images
    """
    if not recommendations:
        return recommendations
    
    print(f"Enrichissement de {len(recommendations)} recommandations avec des images...")
    
    # Créer une copie pour ne pas modifier l'original
    enriched_recommendations = recommendations.copy()
    
    for i, place in enumerate(enriched_recommendations):
        place_name = place.get("nom", "")
        place_type = place.get("type", "")
        
        print(f"\nTraitement de: {place_name}")
        
        # Terme de recherche
        search_term = f"{place_name} {place_type} {location}"
        
        # Obtenir image
        image_url = get_unsplash_image(search_term)
        
        # Ajouter explicitement au dictionnaire
        enriched_recommendations[i]["url_image"] = image_url
        
        # Pause pour éviter les erreurs de rate-limiting
        time.sleep(1)
    
    # Vérification finale
    print("\nEnrichissement terminé.")
    for rec in enriched_recommendations:
        if "url_image" not in rec:
            print(f"ATTENTION: {rec.get('nom', 'Un lieu')} n'a pas d'URL d'image!")
    
    return enriched_recommendations