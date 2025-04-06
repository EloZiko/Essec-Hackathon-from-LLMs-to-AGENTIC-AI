
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
        
        // Animation de swipe à droite
        const recommendationCard = document.querySelector('.recommendation-card');
        recommendationCard.classList.add('swipe-right');
        
        // Ajouter à la liste des recommandations aimées
        likedRecommendations.push(currentRecommendations[currentIndex]);
        
        // Attendre que l'animation soit terminée avant de passer à la suivante
        setTimeout(() => {
            recommendationCard.classList.remove('swipe-right');
            nextRecommendation();
        }, 500); // 500ms correspond à la durée de l'animation CSS
    });
    
    // Gérer le clic sur "Je n'aime pas"
    document.querySelector('.dislike-btn').addEventListener('click', function() {
        if (currentRecommendations.length === 0) return;
        
        // Animation de swipe à gauche
        const recommendationCard = document.querySelector('.recommendation-card');
        recommendationCard.classList.add('swipe-left');
        
        // Attendre que l'animation soit terminée avant de passer à la suivante
        setTimeout(() => {
            recommendationCard.classList.remove('swipe-left');
            nextRecommendation();
        }, 500); // 500ms correspond à la durée de l'animation CSS
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
    
    // Ajouter la gestion des swipes tactiles pour les appareils mobiles
    const recommendationCard = document.querySelector('.recommendation-card');
    if (recommendationCard) {
        let touchStartX = 0;
        let touchEndX = 0;
        
        recommendationCard.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
        });
        
        recommendationCard.addEventListener('touchend', function(e) {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        });
        
        function handleSwipe() {
            if (touchEndX < touchStartX - 50) {
                // Swipe à gauche
                document.querySelector('.dislike-btn').click();
            }
            
            if (touchEndX > touchStartX + 50) {
                // Swipe à droite
                document.querySelector('.like-btn').click();
            }
        }
    }
});
