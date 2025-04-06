"""
Interface web pour le générateur de recommandations utilisant Flask
"""
from flask import Flask, render_template, request, jsonify, session
import os
import json
import traceback
from main import RecommendationService
from config.settings import DEFAULT_LOCATION

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clé pour la session

# Créer les dossiers requis s'ils n'existent pas
if not os.path.exists("templates"):
    os.makedirs("templates")
if not os.path.exists("static"):
    os.makedirs("static")
if not os.path.exists("static/css"):
    os.makedirs("static/css")
if not os.path.exists("static/js"):
    os.makedirs("static/js")

# Créer le fichier HTML principal
with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write("""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recommandations de Sorties</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container-fluid p-0">
        <!-- Header avec gradient -->
        <div class="header">
            <div class="container py-4">
                <h1 class="text-white text-center mb-0">
                    <i class="fas fa-map-marker-alt"></i> Recommandations de Sorties
                </h1>
            </div>
        </div>

        <!-- Section de recherche -->
        <div class="container search-container my-4">
            <div class="card shadow">
                <div class="card-body">
                    <h4 class="card-title mb-3"><i class="fas fa-search"></i> Trouvez votre prochaine sortie</h4>
                    <form id="search-form">
                        <div class="row g-3">
                            <div class="col-md-6">
                                <div class="form-floating mb-3">
                                    <input type="text" class="form-control" id="location" name="location" placeholder="Paris" value="{{ default_location }}">
                                    <label for="location"><i class="fas fa-city"></i> Ville</label>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-floating mb-3">
                                    <input type="text" class="form-control" id="prompt" name="prompt" placeholder="Je veux sortir avec des amis ce soir" required>
                                    <label for="prompt"><i class="fas fa-comment"></i> Que recherchez-vous ?</label>
                                </div>
                            </div>
                        </div>
                        <button type="submit" class="btn btn-primary btn-lg w-100">
                            <i class="fas fa-search"></i> Rechercher
                        </button>
                    </form>
                </div>
            </div>
        </div>

        <!-- Loading spinner -->
        <div id="loading-spinner" class="container text-center d-none">
            <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
                <span class="visually-hidden">Chargement...</span>
            </div>
            <p class="mt-2">Recherche des meilleures recommandations...</p>
        </div>

        <!-- Section des recommandations -->
        <div class="container recommendation-container my-4 d-none">
            <div class="progress mb-3">
                <div class="progress-bar" role="progressbar" style="width: 0%" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
            
            <div class="card shadow recommendation-card">
                <div class="card-body">
                    <h3 class="card-title recommendation-name mb-4 text-center"></h3>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="positives-container">
                                <h5><i class="fas fa-thumbs-up text-success"></i> Points positifs</h5>
                                <ul class="positives-list list-group list-group-flush"></ul>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="negatives-container">
                                <h5><i class="fas fa-thumbs-down text-danger"></i> Points négatifs</h5>
                                <ul class="negatives-list list-group list-group-flush"></ul>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card-footer d-flex justify-content-between">
                    <button class="btn btn-danger dislike-btn">
                        <i class="fas fa-times"></i> Je n'aime pas
                    </button>
                    <div class="counter-text"></div>
                    <button class="btn btn-success like-btn">
                        <i class="fas fa-heart"></i> J'aime
                    </button>
                </div>
            </div>
        </div>

        <!-- Section des résultats finaux -->
        <div class="container results-container my-4 d-none">
            <div class="card shadow">
                <div class="card-body">
                    <h4 class="card-title mb-3"><i class="fas fa-check-circle text-success"></i> Vos recommandations préférées</h4>
                    <div class="liked-recommendations-container">
                        <p class="no-likes-message d-none">Vous n'avez aimé aucune recommandation.</p>
                        <ul class="liked-list list-group list-group-flush"></ul>
                    </div>
                    <button class="btn btn-primary mt-3 new-search-btn">
                        <i class="fas fa-search"></i> Nouvelle recherche
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
""")

# Créer le fichier CSS
with open("static/css/style.css", "w", encoding="utf-8") as f:
    f.write("""
body {
    background-color: #f8f9fa;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header {
    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
    padding: 1rem 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.search-container, .recommendation-container, .results-container {
    max-width: 900px;
}

.recommendation-card {
    transition: all 0.3s ease;
}

.card {
    border-radius: 10px;
    overflow: hidden;
}

.card-title {
    color: #333;
}

.recommendation-name {
    color: #2575fc;
    font-weight: bold;
}

.list-group-item {
    border: none;
    padding: 0.5rem 0;
    position: relative;
}

.list-group-item::before {
    content: "•";
    margin-right: 8px;
    color: #6a11cb;
}

.positives-list .list-group-item::before {
    color: #198754;
}

.negatives-list .list-group-item::before {
    color: #dc3545;
}

.btn-primary {
    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
    border: none;
}

.btn-success {
    background-color: #198754;
}

.btn-danger {
    background-color: #dc3545;
}

.counter-text {
    font-weight: bold;
    align-self: center;
    color: #6c757d;
}

.liked-list .list-group-item {
    margin-bottom: 10px;
    background-color: #f8f9fa;
    border-left: 4px solid #2575fc;
    padding-left: 15px;
}

.btn {
    border-radius: 5px;
    font-weight: 500;
    transition: all 0.2s;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
    .btn {
        padding: 0.5rem;
        font-size: 0.9rem;
    }
}
""")

# Créer le fichier JavaScript
with open("static/js/app.js", "w", encoding="utf-8") as f:
    f.write("""
document.addEventListener('DOMContentLoaded', function() {
    // Éléments DOM
    const searchForm = document.getElementById('search-form');
    const loadingSpinner = document.getElementById('loading-spinner');
    const recommendationContainer = document.querySelector('.recommendation-container');
    const resultsContainer = document.querySelector('.results-container');
    const progressBar = document.querySelector('.progress-bar');
    
    // Données de l'application
    let currentRecommendations = [];
    let currentIndex = 0;
    let likedRecommendations = [];
    
    // Soumettre le formulaire de recherche
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const locationInput = document.getElementById('location');
        const promptInput = document.getElementById('prompt');
        
        const location = locationInput.value.trim();
        const prompt = promptInput.value.trim();
        
        if (!prompt) {
            alert('Veuillez entrer une demande de recherche');
            return;
        }
        
        // Réinitialiser les données
        currentRecommendations = [];
        currentIndex = 0;
        likedRecommendations = [];
        
        // Afficher le spinner de chargement
        loadingSpinner.classList.remove('d-none');
        recommendationContainer.classList.add('d-none');
        resultsContainer.classList.add('d-none');
        
        // Effectuer la requête API
        fetch('/api/recommendations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                location: location,
                prompt: prompt
            })
        })
        .then(response => response.json())
        .then(data => {
            // Cacher le spinner
            loadingSpinner.classList.add('d-none');
            
            if (data.recommendations && data.recommendations.length > 0) {
                currentRecommendations = data.recommendations;
                showRecommendation();
                recommendationContainer.classList.remove('d-none');
            } else {
                alert('Aucune recommandation trouvée. Veuillez essayer avec une autre demande.');
            }
        })
        .catch(error => {
            loadingSpinner.classList.add('d-none');
            console.error('Erreur:', error);
            alert('Une erreur est survenue lors de la recherche de recommandations.');
        });
    });
    
    // Afficher la recommandation actuelle
    function showRecommendation() {
        if (currentRecommendations.length === 0) return;
        
        const recommendation = currentRecommendations[currentIndex];
        
        // Mettre à jour le titre
        document.querySelector('.recommendation-name').textContent = recommendation.name;
        
        // Mettre à jour les points positifs
        const positivesList = document.querySelector('.positives-list');
        positivesList.innerHTML = '';
        recommendation.positives.forEach(point => {
            const li = document.createElement('li');
            li.className = 'list-group-item';
            li.textContent = point;
            positivesList.appendChild(li);
        });
        
        // Mettre à jour les points négatifs
        const negativesList = document.querySelector('.negatives-list');
        negativesList.innerHTML = '';
        recommendation.negatives.forEach(point => {
            const li = document.createElement('li');
            li.className = 'list-group-item';
            li.textContent = point;
            negativesList.appendChild(li);
        });
        
        // Mettre à jour le compteur et la barre de progression
        document.querySelector('.counter-text').textContent = `${currentIndex + 1}/${currentRecommendations.length}`;
        const progressPercentage = ((currentIndex + 1) / currentRecommendations.length) * 100;
        progressBar.style.width = `${progressPercentage}%`;
        progressBar.setAttribute('aria-valuenow', progressPercentage);
    }
    
    // Gérer le clic sur "J'aime"
    document.querySelector('.like-btn').addEventListener('click', function() {
        if (currentRecommendations.length === 0) return;
        
        // Ajouter à la liste des recommandations aimées
        likedRecommendations.push(currentRecommendations[currentIndex]);
        
        // Passer à la recommandation suivante
        nextRecommendation();
    });
    
    // Gérer le clic sur "Je n'aime pas"
    document.querySelector('.dislike-btn').addEventListener('click', function() {
        if (currentRecommendations.length === 0) return;
        
        // Simplement passer à la recommandation suivante
        nextRecommendation();
    });
    
    // Passer à la recommandation suivante
    function nextRecommendation() {
        currentIndex++;
        
        if (currentIndex >= currentRecommendations.length) {
            // Toutes les recommandations ont été vues
            showResults();
        } else {
            // Afficher la recommandation suivante
            showRecommendation();
        }
    }
    
    // Afficher les résultats finaux
    function showResults() {
        recommendationContainer.classList.add('d-none');
        resultsContainer.classList.remove('d-none');
        
        const likedList = document.querySelector('.liked-list');
        const noLikesMessage = document.querySelector('.no-likes-message');
        
        likedList.innerHTML = '';
        
        if (likedRecommendations.length === 0) {
            noLikesMessage.classList.remove('d-none');
        } else {
            noLikesMessage.classList.add('d-none');
            likedRecommendations.forEach(rec => {
                const li = document.createElement('li');
                li.className = 'list-group-item';
                li.textContent = rec.name;
                likedList.appendChild(li);
            });
        }
    }
    
    // Gérer le clic sur "Nouvelle recherche"
    document.querySelector('.new-search-btn').addEventListener('click', function() {
        resultsContainer.classList.add('d-none');
        
        // Réinitialiser le formulaire
        document.getElementById('prompt').value = '';
        document.getElementById('prompt').focus();
    });
});
""")

# Service de recommandations
service = RecommendationService()

@app.route('/')
def index():
    """Page d'accueil de l'application"""
    return render_template('index.html', default_location=DEFAULT_LOCATION)

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """API pour obtenir des recommandations"""
    try:
        data = request.json
        location = data.get('location', DEFAULT_LOCATION)
        if not location or not location.strip():
            location = DEFAULT_LOCATION
            
        user_prompt = data.get('prompt', '')
        if not user_prompt:
            return jsonify({
                'status': 'error',
                'message': 'Veuillez fournir une demande de recherche'
            }), 400
        
        print(f"Génération des recommandations pour: '{user_prompt}' à {location}")
        
        # Obtenir les recommandations
        recommendations = service.get_recommendations(user_prompt, location)
        
        print(f"Recommandations reçues: {len(recommendations) if recommendations else 0}")
        
        # S'assurer que les recommandations sont sérialisables
        clean_recommendations = []
        
        # Vérifier si recommendations est une liste
        if not isinstance(recommendations, list):
            print(f"Les recommandations ne sont pas sous forme de liste: {type(recommendations)}")
            # Essayer de convertir en liste si c'est un dictionnaire unique
            if isinstance(recommendations, dict):
                recommendations = [recommendations]
            else:
                # Essayer de parser depuis JSON si c'est une chaîne
                try:
                    if isinstance(recommendations, str):
                        import json
                        parsed = json.loads(recommendations)
                        if isinstance(parsed, list):
                            recommendations = parsed
                        elif isinstance(parsed, dict) and 'recommendations' in parsed:
                            recommendations = parsed['recommendations']
                        else:
                            recommendations = [parsed]
                except Exception as parse_error:
                    print(f"Erreur lors de la conversion en JSON: {str(parse_error)}")
                    recommendations = []
        
        for i, rec in enumerate(recommendations):
            print(f"Traitement recommandation {i+1}: {rec.get('name', 'Sans nom')}")
            
            # S'assurer que chaque recommandation a les champs nécessaires
            clean_rec = {
                'name': rec.get('name', f'Recommandation {i+1}'),
                'positives': [],
                'negatives': []
            }
            
            # Vérifier et formater les points positifs
            if 'positives' in rec:
                positives = rec['positives']
                if isinstance(positives, list):
                    clean_rec['positives'] = positives
                elif isinstance(positives, str):
                    # Si c'est une chaîne unique, la transformer en liste
                    clean_rec['positives'] = [positives]
                else:
                    # Pour tout autre type, convertir en chaîne
                    clean_rec['positives'] = [str(positives)]
            else:
                # Chercher d'autres clés possibles
                for key in ['pros', 'avantages', 'points_positifs', 'advantages']:
                    if key in rec:
                        positives = rec[key]
                        if isinstance(positives, list):
                            clean_rec['positives'] = positives
                            break
                        elif isinstance(positives, str):
                            clean_rec['positives'] = [positives]
                            break
                        else:
                            clean_rec['positives'] = [str(positives)]
                            break
            
            # Vérifier et formater les points négatifs
            if 'negatives' in rec:
                negatives = rec['negatives']
                if isinstance(negatives, list):
                    clean_rec['negatives'] = negatives
                elif isinstance(negatives, str):
                    clean_rec['negatives'] = [negatives]
                else:
                    clean_rec['negatives'] = [str(negatives)]
            else:
                # Chercher d'autres clés possibles
                for key in ['cons', 'inconvénients', 'points_négatifs', 'disadvantages']:
                    if key in rec:
                        negatives = rec[key]
                        if isinstance(negatives, list):
                            clean_rec['negatives'] = negatives
                            break
                        elif isinstance(negatives, str):
                            clean_rec['negatives'] = [negatives]
                            break
                        else:
                            clean_rec['negatives'] = [str(negatives)]
                            break
            
            # S'assurer qu'il y a au moins un point positif et négatif
            if not clean_rec['positives']:
                clean_rec['positives'] = ["Information non disponible"]
            
            if not clean_rec['negatives']:
                clean_rec['negatives'] = ["Information non disponible"]
                
            clean_recommendations.append(clean_rec)
        
        # Garantir au moins une recommandation
        if not clean_recommendations:
            print("Aucune recommandation valide, création d'une recommandation par défaut")
            clean_recommendations = [{
                'name': f"Suggestion pour {location}",
                'positives': ["Recommandation basée sur votre recherche"],
                'negatives': ["Pas d'informations détaillées disponibles"]
            }]
        
        # Stocker les recommandations dans la session
        session['recommendations'] = clean_recommendations
        
        print(f"Envoi de {len(clean_recommendations)} recommandations à l'interface")
        
        # Retourner la réponse
        return jsonify({
            'status': 'success',
            'recommendations': clean_recommendations
        })
    except Exception as e:
        print(f"Erreur lors du traitement de la requête: {str(e)}")
        traceback.print_exc()  # Afficher la stack trace complète
        return jsonify({
            'status': 'error',
            'message': f"Une erreur est survenue: {str(e)}"
        }), 500
        
# Ajouter à la fin du fichier:

if __name__ == "__main__":
    print("Serveur lancé sur http://127.0.0.1:5000")
    print("Appuyez sur Ctrl+C pour quitter")
    app.run(debug=True)