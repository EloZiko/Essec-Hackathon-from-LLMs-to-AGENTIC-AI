"""
Interface en ligne de commande pour le générateur de recommandations
"""
import argparse
from main import RecommendationService
from config.settings import DEFAULT_OUTPUT_FORMAT, DEFAULT_LOCATION

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
        default=DEFAULT_OUTPUT_FORMAT,
        help="Format de sortie (json ou text)"
    )
    
    parser.add_argument(
        "--location", 
        type=str, 
        default=DEFAULT_LOCATION,
        help="Ville pour les recommandations (défaut: Paris)"
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
    service = RecommendationService()
    results = service.get_formatted_recommendations(
        user_prompt, 
        output_format=args.format,
        location=args.location
    )
    
    # Afficher les résultats
    if args.format == "text":
        print("-" * 50)
        print(results)
        print("-" * 50)
        print(f"✨ Profitez de votre sortie à {args.location}! ✨")
    else:
        print(results)
    
    return service.get_recommendations(user_prompt, args.location)

if __name__ == "__main__":
    recommendations = main()