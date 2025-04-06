"""
Utility functions for the recommendation GUI application.
"""

def format_recommendation_data(recommendation):
    """
    Formats the recommendation data for display in the GUI.
    
    Args:
        recommendation (dict): A dictionary containing recommendation details.
        
    Returns:
        str: Formatted string representation of the recommendation.
    """
    return f"{recommendation['name']} - {recommendation['location']}\nDescription: {recommendation['description']}\n"

def validate_user_input(input_text):
    """
    Validates user input to ensure it is not empty.
    
    Args:
        input_text (str): The input text from the user.
        
    Returns:
        bool: True if the input is valid, False otherwise.
    """
    return bool(input_text.strip())

def extract_positive_negative_points(recommendation):
    """
    Extracts positive and negative points from a recommendation.
    
    Args:
        recommendation (dict): A dictionary containing recommendation details.
        
    Returns:
        tuple: A tuple containing lists of positive and negative points.
    """
    positive_points = recommendation.get('points_positifs', [])
    negative_points = recommendation.get('points_negatifs', [])
    return positive_points, negative_points
"""