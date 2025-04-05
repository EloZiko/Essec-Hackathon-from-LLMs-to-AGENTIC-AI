"""
Module principal contenant la logique de l'application
"""
from core.llm_service import MistralService
from config.settings import DEFAULT_LOCATION
from utils.formatters import format_as_text, format_as_json
import argparse
import time
import json
import requests
from urllib.parse import quote_plus
import sys


# Fonction d'enrichissement directement dans main.py pour éviter les problèmes d'importation
def get_unsplash_image(search_term):
    """
    Récupère une image Unsplash aléatoire
    
    Args:
        search_term (str): Le terme de recherche
        
    Returns:
        str: URL de l'image ou image par défaut
    """
    try:
        encoded_term = quote_plus(search_term)
        url = f"https://source.unsplash.com/random/?{encoded_term}"
        
        # Utiliser une requête HEAD pour ne pas télécharger l'image
        response = requests.head(url, allow_redirects=True)
        
        # Vérifier si la requête a réussi
        if response.status_code == 200:
            final_url = response.url
            return final_url
            
    except Exception as e:
        print(f"Erreur: {e}")
    
    # Image par défaut si échec
    return "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad"

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
    
    print("Ajout d'images aux recommandations...")
    
    # Créer une copie profonde pour éviter de modifier l'original
    import copy
    enriched_recommendations = copy.deepcopy(recommendations)
    
    for i, place in enumerate(enriched_recommendations):
        place_name = place.get("nom", "")
        place_type = place.get("type", "")
        
        # Terme de recherche
        search_term = f"{place_name} {place_type} {location}"
        
        # Obtenir image
        image_url = get_unsplash_image(search_term)
        
        # Ajouter explicitement au dictionnaire
        enriched_recommendations[i]["url_image"] = image_url
        
        # Pause pour éviter les erreurs de rate-limiting
        time.sleep(0.5)
    
    print("Enrichissement terminé.")
    return enriched_recommendations

class RecommendationService:
    """Service principal de recommandation"""
    
    def __init__(self):
        """Initialise le service de recommandation"""
        self.mistral_service = MistralService()
    
    def get_recommendations(self, user_prompt, location=DEFAULT_LOCATION, with_images=False):
        """
        Obtient des recommandations de lieux
        
        Args:
            user_prompt (str): Requête utilisateur
            location (str): Ville pour les recommandations
            with_images (bool): Si True, ajoute des URLs d'images aux recommandations
            
        Returns:
            list: Liste de dictionnaires de recommandations
        """
        # Obtenir les recommandations du LLM
        recommendations = self.mistral_service.generate_recommendations(user_prompt, location)
        
        # Ajouter des images si demandé
        if with_images and recommendations:
            print("Enrichissement des recommandations avec des images...")
            recommendations = enrich_recommendations_with_images(recommendations, location)
        
        return recommendations
    
    def get_formatted_recommendations(self, user_prompt, output_format="json", location=DEFAULT_LOCATION, with_images=False):
        """
        Obtient des recommandations formatées
        
        Args:
            user_prompt (str): Requête utilisateur
            output_format (str): Format de sortie ("json" ou "text")
            location (str): Ville pour les recommandations
            with_images (bool): Si True, ajoute des URLs d'images aux recommandations
            
        Returns:
            str: Recommandations formatées selon le format demandé
        """
        recommendations = self.get_recommendations(user_prompt, location, with_images)
        
        if output_format == "json":
            return format_as_json(recommendations)
        else:
            return format_as_text(recommendations)

def main():
    """Point d'entrée principal pour l'interface en ligne de commande"""
    parser = argparse.ArgumentParser(
        description="Générateur de recommandations de sorties personnalisées"
    )
    
    parser.add_argument(
        "--prompt", 
        type=str, 
        help="Votre demande de recommandation"
    )
    
    parser.add_argument(
        "--format", 
        type=str, 
        choices=["json", "text"], 
        default="json",
        help="Format de sortie (json ou text)"
    )
    
    parser.add_argument(
        "--location", 
        type=str, 
        default=DEFAULT_LOCATION,
        help="Ville pour les recommandations (défaut: Paris)"
    )
    
    parser.add_argument(
        "--images",
        action="store_true",
        help="Inclure des URLs d'images dans les recommandations"
    )
    
    args = parser.parse_args()
    
    # Afficher l'en-tête si sortie texte
    if args.format == "text":
        print(f"🌆 RECOMMANDATIONS DE SORTIES À {args.location.upper()} 🌆")
        print("-" * 50)
    
    # Obtenir le prompt utilisateur
    if args.prompt:
        user_prompt = args.prompt
    else:
        user_prompt = input(f"\nQue souhaitez-vous faire à {args.location}? (Ex: 'je veux sortir ce soir avec des amis boire un verre')\n> ")
    
    if args.format == "text":
        print("\nGénération des recommandations en cours...")
    
    # Initialiser le service et obtenir les recommandations
    start_time = time.time()
    service = RecommendationService()
    
    # Obtenir les recommandations une seule fois
    recommendations = service.get_recommendations(user_prompt, args.location, args.images)
    
    # Formater pour l'affichage
    if args.format == "json":
        formatted_results = json.dumps(recommendations, indent=2, ensure_ascii=False)
    else:
        formatted_results = format_as_text(recommendations)
    
    # Afficher les résultats formatés
    if args.format == "text":
        print("-" * 50)
        print(formatted_results)
        print("-" * 50)
        print(f"✨ Profitez de votre sortie à {args.location}! ✨")
    else:
        print(formatted_results)
    
    # Si des images ont été demandées, afficher le temps d'exécution
    if args.images:
        elapsed = time.time() - start_time
        print(f"\nTemps total d'exécution: {elapsed:.2f} secondes")
    
    # Retourner les recommandations non formatées (avec les images)
    return recommendations

if __name__ == "__main__":
    # Installer les packages nécessaires si manquants
    try:
        import requests
    except ImportError:
        import subprocess
        import sys
        print("Installation du package 'requests'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests
    
    # Exécuter le programme
    recommendations = main()
    