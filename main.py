"""
Module principal contenant la logique de l'application
"""
from core.llm_service import MistralService
from config.settings import DEFAULT_LOCATION
from utils.formatters import format_as_text, format_as_json
import argparse

class RecommendationService:
    """Service principal de recommandation"""
    
    def __init__(self):
        """Initialise le service de recommandation"""
        self.mistral_service = MistralService()
    
    def get_recommendations(self, user_prompt, location=DEFAULT_LOCATION):
        """
        Obtient des recommandations de lieux
        
        Args:
            user_prompt (str): Requête utilisateur
            location (str): Ville pour les recommandations
            
        Returns:
            list: Liste de dictionnaires de recommandations
        """
        return self.mistral_service.generate_recommendations(user_prompt, location)
    
    def get_formatted_recommendations(self, user_prompt, output_format="json", location=DEFAULT_LOCATION):
        """
        Obtient des recommandations formatées
        
        Args:
            user_prompt (str): Requête utilisateur
            output_format (str): Format de sortie ("json" ou "text")
            location (str): Ville pour les recommandations
            
        Returns:
            str: Recommandations formatées selon le format demandé
        """
        recommendations = self.get_recommendations(user_prompt, location)
        
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
        help="Ville pour les recommandations (Ex: Paris, Lyon, Marseille, etc.)"
    )
    
    args = parser.parse_args()
    
    # Déterminer la localisation
    if args.location:
        location = args.location
    else:
        location = input("\nDans quelle ville recherchez-vous des recommandations? (Ex: Paris, Lyon, Marseille, etc.)\n> ")
        if not location.strip():
            location = DEFAULT_LOCATION
            print(f"\nAucune ville spécifiée, utilisation de la ville par défaut: {location}")
    
    # Afficher l'en-tête si sortie texte
    if args.format == "text":
        print(f"🌆 RECOMMANDATIONS DE SORTIES À {location.upper()} 🌆")
        print("-" * 50)
    
    # Obtenir le prompt utilisateur
    if args.prompt:
        user_prompt = args.prompt
    else:
        user_prompt = input(f"\nQue souhaitez-vous faire à {location}? (Ex: 'je veux sortir ce soir avec des amis boire un verre')\n> ")
    
    if args.format == "text":
        print(f"\nGénération des recommandations pour {location} en cours...")
    
    # Initialiser le service et obtenir les recommandations
    service = RecommendationService()
    results = service.get_formatted_recommendations(
        user_prompt, 
        output_format=args.format,
        location=location
    )
    
    # Afficher les résultats
    if args.format == "text":
        print("-" * 50)
        print(results)
        print("-" * 50)
        print(f"✨ Profitez de votre sortie à {location}! ✨")
    else:
        print(results)
    
    return service.get_recommendations(user_prompt, location)

if __name__ == "__main__":
    # Ce bloc s'exécute uniquement lorsque le script est lancé directement
    recommendations = main()