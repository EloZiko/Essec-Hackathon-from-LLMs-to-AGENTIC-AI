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
        
    
    import json


    
    def generate_itinerary(self, user_prompt, location):
        """
        Génère un itinéraire complet pour la journée
        
        Args:
            user_prompt (str): Demande de l'utilisateur
            location (str): Ville pour les recommandations
            
        Returns:
            dict: Itinéraire structuré avec activités et restaurants
        """
        # Construire le prompt pour le LLM
        prompt = f"""Génère un itinéraire touristique détaillé pour {location} basé sur cette demande: "{user_prompt}".

L'itinéraire doit être au format JSON exact suivant sans aucun texte supplémentaire:
{{
    "morning_activities": [
        {{
            "name": "Nom du lieu",
            "description": "Description de 1-2 phrases",
            "address": "Adresse précise",
            "popularity": X,  // Coefficient de popularité entre 1-10
            "preference": Y   // 0 ou 1 selon si ça correspond aux préférences utilisateur
        }},
        // 2-3 activités du matin
    ],
    "lunch_restaurants": [
        {{
            "name": "Nom du restaurant",
            "description": "Description de 1-2 phrases",
            "address": "Adresse précise",
            "popularity": X,  // Coefficient de popularité entre 1-10
            "preference": Y   // 0 ou 1 selon si ça correspond aux préférences utilisateur
        }},
        // 2-3 restaurants pour le déjeuner
    ],
    "afternoon_activities": [
        // Même structure, 2-3 activités
    ],
    "dinner_restaurants": [
        // Même structure, 2-3 restaurants
    ]
}}

Notes importantes:
- Le coefficient de popularité va de 1 à 10 (10 = très populaire comme la Tour Eiffel à Paris)
- Le coefficient de préférence est 1 si l'élément correspond parfaitement à la demande de l'utilisateur, sinon 0
- Génère des adresses précises et réelles
- Assure-toi que toutes les suggestions sont pertinentes pour {location}
- Réponds UNIQUEMENT avec le JSON, sans texte avant ou après
"""
        
        try:
            # Afficher le debug pour voir si le prompt est bien envoyé
            print("Envoi de la requête à l'API Mistral...")
            
            # Génération de la réponse
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "Tu es un assistant de voyage spécialisé qui génère des itinéraires précis au format JSON structuré."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7,  # Ajuster la température pour plus de créativité mais moins de hallucinations
                max_tokens=2048   # Assurer suffisamment de tokens pour la réponse complète
            )
            
            # Extraire et parser la réponse JSON
            content = response.choices[0].message.content.strip()
            
            # Debug: afficher le début du contenu reçu
            print(f"Réponse reçue (premiers 100 caractères): {content[:100]}...")
            
            # Parser le JSON
            itinerary = json.loads(content)
            
            # Vérifier que l'itinéraire contient bien des données
            if (not itinerary.get("morning_activities") and 
                not itinerary.get("lunch_restaurants") and
                not itinerary.get("afternoon_activities") and
                not itinerary.get("dinner_restaurants")):
                # Fallback si le JSON est vide
                return self._generate_fallback_itinerary(user_prompt, location)
                
            return itinerary
            
        except Exception as e:
            print(f"Erreur lors de la génération de l'itinéraire: {str(e)}")
            # En cas d'erreur, générer un itinéraire de secours
            return self._generate_fallback_itinerary(user_prompt, location)
    
    def _generate_fallback_itinerary(self, user_prompt, location):
        """Génère un itinéraire minimal de secours en cas d'échec"""
        print("Génération d'un itinéraire de secours...")
        
        # Itinéraire de secours avec quelques éléments génériques
        return {
            "morning_activities": [
                {
                    "name": f"Visite du centre-ville de {location}",
                    "description": f"Exploration des rues principales et des monuments du centre de {location}.",
                    "address": f"Place centrale, {location}",
                    "popularity": 8,
                    "preference": 1
                },
                {
                    "name": f"Musée principal de {location}",
                    "description": f"Le musée le plus important de {location}, avec des collections variées.",
                    "address": f"Rue du Musée, {location}",
                    "popularity": 7,
                    "preference": 0
                }
            ],
            "lunch_restaurants": [
                {
                    "name": f"Restaurant local à {location}",
                    "description": "Restaurant populaire servant des spécialités locales.",
                    "address": f"10 Rue Principale, {location}",
                    "popularity": 8,
                    "preference": 1
                },
                {
                    "name": "Café de la Place",
                    "description": "Café-restaurant avec terrasse offrant des plats simples et de qualité.",
                    "address": f"Place centrale, {location}",
                    "popularity": 6,
                    "preference": 0
                }
            ],
            "afternoon_activities": [
                {
                    "name": f"Parc municipal de {location}",
                    "description": f"Espace vert agréable pour se détendre au cœur de {location}.",
                    "address": f"Avenue du Parc, {location}",
                    "popularity": 6,
                    "preference": 0
                },
                {
                    "name": "Shopping",
                    "description": f"Rue commerçante principale de {location} avec boutiques locales et internationales.",
                    "address": f"Rue du Commerce, {location}",
                    "popularity": 7,
                    "preference": 0
                }
            ],
            "dinner_restaurants": [
                {
                    "name": f"Restaurant gastronomique de {location}",
                    "description": "Restaurant élégant proposant une cuisine raffinée.",
                    "address": f"15 Avenue Gourmande, {location}",
                    "popularity": 9,
                    "preference": 1
                },
                {
                    "name": "Bistrot du Coin",
                    "description": "Ambiance conviviale et plats traditionnels de qualité.",
                    "address": f"8 Rue des Gourmets, {location}",
                    "popularity": 7,
                    "preference": 0
                }
            ]
        }