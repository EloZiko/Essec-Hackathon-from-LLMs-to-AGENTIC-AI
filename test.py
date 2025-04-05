from mistralai import Mistral
import argparse
import json

# Clé API Mistral
API_KEY = "DnCAyOg2sUZx3jIwSASA9GWLByW1sanp"
MODEL = "mistral-large-latest"

# Initialiser le client Mistral
client = Mistral(api_key=API_KEY)

def generate_recommendations(user_prompt):
    """
    Génère des recommandations de lieux à Paris basées sur le prompt de l'utilisateur
    
    Args:
        user_prompt (str): La demande de l'utilisateur (ex: "je veux sortir ce soir avec des amis boire un verre à Paris")
        
    Returns:
        list: Liste de dictionnaires contenant les recommandations
    """
    # Enrichir le prompt pour obtenir des recommandations plus structurées
    enhanced_prompt = f"""
    En tant qu'expert local parisien, je recherche des recommandations détaillées et structurées basées sur cette demande:
    "{user_prompt}"
    
    Génère une liste de 5 endroits spécifiques qui correspondent parfaitement à cette demande.
    
    Pour chaque lieu recommandé, tu dois fournir exactement la structure suivante au format JSON:
    
    ```json
    [
      {{
        "type": "Type d'établissement (restaurant, bar, musée, etc.)",
        "nom": "Nom du lieu",
        "adresse": "Adresse complète",
        "quartier": "Quartier/arrondissement",
        "points_positifs": [
          "Point positif 1 concernant le prix, l'ambiance, les avis Google Maps, etc.",
          "Point positif 2", 
          "Point positif 3"
        ],
        "points_negatifs": [
          "Point négatif 1 (horaires, affluence, prix, etc.)",
          "Point négatif 2"
        ]
      }},
      {{
        // Lieu suivant
      }}
    ]
    ```
    
    Inclus 3-4 points positifs et 2 points négatifs spécifiques pour chaque lieu.
    N'invente pas de lieux - ne recommande que des endroits authentiques qui existent réellement à Paris en 2025.
    Retourne UNIQUEMENT le JSON valide, sans aucun texte d'introduction ou de conclusion.
    """
    
    try:
        # Appel à l'API Mistral
        response = client.chat.complete(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Tu es un expert local parisien qui connaît parfaitement tous les bars, restaurants et lieux de sortie de la capitale. Tu réponds uniquement au format JSON demandé, sans texte supplémentaire."},
                {"role": "user", "content": enhanced_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        # Récupérer le contenu et nettoyer pour obtenir JSON valide
        content = response.choices[0].message.content.strip()
        
        # Extraire le JSON s'il est entouré de délimiteurs de bloc de code
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        # Parser le JSON
        try:
            recommendations = json.loads(content)
            return recommendations  # Retourne directement la liste de dictionnaires
        except json.JSONDecodeError:
            return [{"erreur": "Format JSON invalide", "reponse_brute": content}]
            
    except Exception as e:
        return [{"erreur": f"Erreur lors de la génération des recommandations: {str(e)}"}]

def format_recommendations_for_display(recommendations):
    """
    Formate les recommandations JSON en texte lisible pour affichage
    
    Args:
        recommendations (list): Liste de dictionnaires contenant les recommandations
        
    Returns:
        str: Texte formaté des recommandations
    """
    formatted_text = ""
    
    for i, place in enumerate(recommendations, 1):
        if "erreur" in place:
            return f"Erreur: {place.get('erreur')}\n{place.get('reponse_brute', '')}"
            
        place_type = place.get('type', 'Non spécifié')
        formatted_text += f"🌟 {i}. {place.get('nom')} - {place_type} - {place.get('quartier')}\n"
        formatted_text += f"Adresse: {place.get('adresse', 'Non spécifiée')}\n\n"
        
        formatted_text += "Points positifs:\n"
        for point in place.get('points_positifs', []):
            formatted_text += f"  ✓ {point}\n"
        
        formatted_text += "\nPoints négatifs:\n"
        for point in place.get('points_negatifs', []):
            formatted_text += f"  ✗ {point}\n"
        
        formatted_text += "\n" + "-" * 40 + "\n\n"
    
    return formatted_text

def main():
    """Interface principale du programme"""
    parser = argparse.ArgumentParser(description="Générateur de recommandations de sorties à Paris")
    parser.add_argument("--prompt", type=str, help="Votre demande de recommandation")
    parser.add_argument("--format", type=str, choices=["json", "text"], default="text", 
                      help="Format de sortie (json ou text)")
    args = parser.parse_args()
    
    print("🗼 RECOMMANDATIONS DE SORTIES À PARIS 🗼")
    print("-" * 50)
    
    if args.prompt:
        user_prompt = args.prompt
    else:
        user_prompt = input("\nQue souhaitez-vous faire à Paris? (Ex: 'je veux sortir ce soir avec des amis boire un verre à Paris')\n> ")
    
    print("\nGénération des recommandations en cours...")
    
    recommendations = generate_recommendations(user_prompt)
    
    # Afficher les résultats selon le format demandé
    if args.format == "json":
        # Sortie en JSON pour utilisation programmatique
        print(json.dumps(recommendations, indent=2, ensure_ascii=False))
    else:
        # Sortie formatée texte pour lecture humaine
        print("-" * 50)
        print(format_recommendations_for_display(recommendations))
        print("-" * 50)
        print("✨ Profitez de votre soirée parisienne! ✨")
        
    # Retourne aussi la liste de dictionnaires pour une utilisation programmatique
    return recommendations

if __name__ == "__main__":
    result = main()