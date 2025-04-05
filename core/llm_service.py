"""
Service d'interaction avec les LLM pour générer des recommandations
"""
from mistralai import Mistral
import json
from config.settings import MISTRAL_API_KEY, MISTRAL_MODEL, TEMPERATURE, MAX_TOKENS
from core.recommendation import Recommendation

class MistralService:
    """Service d'interaction avec l'API Mistral"""
    
    def __init__(self, api_key=MISTRAL_API_KEY, model=MISTRAL_MODEL):
        """
        Initialise le service Mistral
        
        Args:
            api_key (str): Clé API Mistral
            model (str): Modèle Mistral à utiliser
        """
        self.api_key = api_key
        self.model = model
        self.client = Mistral(api_key=self.api_key)
    
    def build_prompt(self, user_prompt, location="Paris"):
        """
        Construit le prompt pour générer des recommandations
        
        Args:
            user_prompt (str): Requête de l'utilisateur
            location (str): Nom de la ville
            
        Returns:
            str: Prompt enrichi
        """
        return f"""
        En tant qu'expert local de {location}, je recherche des recommandations détaillées et structurées basées sur cette demande:
        "{user_prompt}"
        
        Génère une liste de 5 endroits spécifiques qui correspondent parfaitement à cette demande.
        
        Pour chaque lieu recommandé, tu dois fournir exactement la structure suivante au format JSON, sans aucune variation:
        
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
          // Et ainsi de suite pour les autres lieux
        ]
        ```
        
        Inclus 3-4 points positifs et 2 points négatifs spécifiques pour chaque lieu.
        N'invente pas de lieux - ne recommande que des endroits authentiques qui existent réellement à {location} en 2025.
        IMPORTANT: Retourne UNIQUEMENT le JSON valide, sans aucun texte d'introduction ou de conclusion.
        """
    
    def get_system_message(self, location="Paris"):
        """
        Définit le message système pour Mistral
        
        Args:
            location (str): Nom de la ville
            
        Returns:
            str: Message système
        """
        return f"Tu es un expert local de {location} qui connaît parfaitement tous les bars, restaurants et lieux de sortie. Tu réponds UNIQUEMENT au format JSON demandé, sans aucun texte supplémentaire. Tu fournis un JSON parfaitement valide qui peut être parsé directement."
    
    def generate_recommendations(self, user_prompt, location="Paris"):
        """
        Génère des recommandations via l'API Mistral
        
        Args:
            user_prompt (str): Requête utilisateur
            location (str): Ville pour les recommandations
            
        Returns:
            list: Liste de dictionnaires de recommandations
        """
        enhanced_prompt = self.build_prompt(user_prompt, location)
        
        try:
            # Appel à l'API Mistral
            response = self.client.chat.complete(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.get_system_message(location)},
                    {"role": "user", "content": enhanced_prompt}
                ],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS
            )
            
            # Récupérer le contenu
            content = response.choices[0].message.content.strip()
            
            # Extraire le JSON
            json_content = self._extract_json(content)
            
            # Parser et valider le JSON
            try:
                recommendations = json.loads(json_content)
                return Recommendation.validate_json(recommendations)
            except json.JSONDecodeError:
                return [Recommendation.create_error(f"Format JSON invalide dans la réponse")]
                
        except Exception as e:
            return [Recommendation.create_error(f"Erreur lors de la génération des recommandations: {str(e)}")]
    
    def _extract_json(self, content):
        """
        Extrait le contenu JSON d'une chaîne de caractères
        
        Args:
            content (str): Contenu brut de la réponse
            
        Returns:
            str: Contenu JSON nettoyé
        """
        if "```json" in content:
            return content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            return content.split("```")[1].split("```")[0].strip()
        return content