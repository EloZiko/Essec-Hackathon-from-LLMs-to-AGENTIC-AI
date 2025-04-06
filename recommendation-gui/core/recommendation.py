"""
Module contenant les classes et fonctions liées aux recommandations
"""

class Recommendation:
    """
    Classe représentant une recommandation de lieu
    """
    def __init__(self, data):
        """
        Initialise une recommandation
        
        Args:
            data (dict): Données de la recommandation
        """
        self.type = data.get("type", "Non spécifié")
        self.nom = data.get("nom", "")
        self.adresse = data.get("adresse", "")
        self.quartier = data.get("quartier", "")
        self.points_positifs = data.get("points_positifs", [])
        self.points_negatifs = data.get("points_negatifs", [])
        
    def to_dict(self):
        """
        Convertit la recommandation en dictionnaire
        
        Returns:
            dict: Dictionnaire représentant la recommandation
        """
        return {
            "type": self.type,
            "nom": self.nom,
            "adresse": self.adresse,
            "quartier": self.quartier,
            "points_positifs": self.points_positifs,
            "points_negatifs": self.points_negatifs
        }
    
    @staticmethod
    def validate_json(recommendations):
        """
        Valide et normalise les recommandations reçues sous forme JSON
        
        Args:
            recommendations (list): Liste de dictionnaires de recommandations
            
        Returns:
            list: Liste de dictionnaires validés et normalisés
        """
        for i, place in enumerate(recommendations):
            # S'assurer que tous les champs requis sont présents
            if "type" not in place:
                place["type"] = "Non spécifié"
            if "nom" not in place:
                place["nom"] = f"Lieu {i+1}"
            if "adresse" not in place:
                place["adresse"] = "Adresse non spécifiée"
            if "quartier" not in place:
                place["quartier"] = "Quartier non spécifié"
            if "points_positifs" not in place:
                place["points_positifs"] = []
            if "points_negatifs" not in place:
                place["points_negatifs"] = []
        
        return recommendations
    
    @classmethod
    def create_error(cls, error_message):
        """
        Crée une recommandation d'erreur
        
        Args:
            error_message (str): Message d'erreur
            
        Returns:
            dict: Recommandation d'erreur
        """
        return {
            "type": "erreur",
            "nom": "Erreur",
            "adresse": "",
            "quartier": "",
            "points_positifs": [],
            "points_negatifs": [error_message]
        }