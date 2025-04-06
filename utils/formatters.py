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


def format_as_text(itinerary):
    """
    Formate un itinéraire en texte lisible
    
    Args:
        itinerary (dict): Itinéraire structuré
    
    Returns:
        str: Itinéraire formaté en texte
    """
    result = []
    
    # Activités du matin
    result.append("🌅 ACTIVITÉS DU MATIN")
    result.append("-" * 40)
    for item in itinerary.get("morning_activities", []):
        result.append(f"📍 {item['name']} (Popularité: {item['popularity']}/10)")
        result.append(f"   {item['description']}")
        result.append(f"   📌 {item['address']}")
        if item['preference'] == 1:
            result.append(f"   ⭐ Recommandé selon vos préférences!")
        result.append("")
    
    # Restaurants pour le déjeuner
    result.append("🍽️ RESTAURANTS POUR LE DÉJEUNER")
    result.append("-" * 40)
    for item in itinerary.get("lunch_restaurants", []):
        result.append(f"🍴 {item['name']} (Popularité: {item['popularity']}/10)")
        result.append(f"   {item['description']}")
        result.append(f"   📌 {item['address']}")
        if item['preference'] == 1:
            result.append(f"   ⭐ Recommandé selon vos préférences!")
        result.append("")
    
    # Activités de l'après-midi
    result.append("☀️ ACTIVITÉS DE L'APRÈS-MIDI")
    result.append("-" * 40)
    for item in itinerary.get("afternoon_activities", []):
        result.append(f"📍 {item['name']} (Popularité: {item['popularity']}/10)")
        result.append(f"   {item['description']}")
        result.append(f"   📌 {item['address']}")
        if item['preference'] == 1:
            result.append(f"   ⭐ Recommandé selon vos préférences!")
        result.append("")
    
    # Restaurants pour le dîner
    result.append("🌙 RESTAURANTS POUR LE DÎNER")
    result.append("-" * 40)
    for item in itinerary.get("dinner_restaurants", []):
        result.append(f"🍴 {item['name']} (Popularité: {item['popularity']}/10)")
        result.append(f"   {item['description']}")
        result.append(f"   📌 {item['address']}")
        if item['preference'] == 1:
            result.append(f"   ⭐ Recommandé selon vos préférences!")
        result.append("")
    
    return "\n".join(result)

def format_as_json(itinerary):
    """
    Formate un itinéraire au format JSON
    
    Args:
        itinerary (dict): Itinéraire structuré
    
    Returns:
        str: Itinéraire au format JSON
    """
    return json.dumps(itinerary, ensure_ascii=False, indent=2)