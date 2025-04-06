from core.llm_service import MistralService
from utils.formatters import format_as_text, format_as_json

class RecommendationController:
    def __init__(self, results_panel, search_panel):
        self.results_panel = results_panel
        self.search_panel = search_panel
        self.mistral_service = MistralService()

        self.search_panel.bind_search(self.generate_recommendations)

    def generate_recommendations(self, user_prompt, location):
        recommendations = self.mistral_service.generate_recommendations(user_prompt, location)
        self.update_results_panel(recommendations)

    def update_results_panel(self, recommendations):
        formatted_recommendations = format_as_json(recommendations)
        self.results_panel.display_recommendations(formatted_recommendations)

    def like_recommendation(self, recommendation):
        self.results_panel.add_to_liked(recommendation)

    def dislike_recommendation(self, recommendation):
        self.results_panel.add_to_disliked(recommendation)