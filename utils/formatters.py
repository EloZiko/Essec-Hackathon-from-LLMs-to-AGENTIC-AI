"""
Fonctions utilitaires pour formater les sorties
"""
import json

def format_as_text(recommendations):
    """
    Formate les recommandations en texte lisible pour l'utilisateur
    
    Args:
        recommendations (list): Liste de dictionnaires de recommandations
        
    Returns:
        str: Texte formaté des recommandations
    """
    formatted_text = ""
    
    for i, place in enumerate(recommendations, 1):
        if place.get("type", "").lower() == "erreur":
            return f"⚠️ Erreur: {place.get('nom')}\nDétails: {', '.join(place.get('points_negatifs', []))}"
            
        place_type = place.get('type', 'Non spécifié')
        formatted_text += f"🌟 {i}. {place.get('nom')} - {place_type} - {place.get('quartier')}\n"
        formatted_text += f"📍 {place.get('adresse', 'Adresse non spécifiée')}\n\n"
        
        formatted_text += "✅ Points positifs:\n"
        for point in place.get('points_positifs', []):
            formatted_text += f"  • {point}\n"
        
        formatted_text += "\n❌ Points négatifs:\n"
        for point in place.get('points_negatifs', []):
            formatted_text += f"  • {point}\n"
        
        formatted_text += "\n" + "-" * 40 + "\n\n"
    
    return formatted_text

def format_as_json(recommendations, indent=2):
    """
    Formate les recommandations en JSON
    
    Args:
        recommendations (list): Liste de dictionnaires de recommandations
        indent (int): Nombre d'espaces pour l'indentation
        
    Returns:
        str: Chaîne JSON formatée
    """
    return json.dumps(recommendations, indent=indent, ensure_ascii=False)