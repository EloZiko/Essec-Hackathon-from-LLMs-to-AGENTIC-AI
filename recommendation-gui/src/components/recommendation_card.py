class RecommendationCard:
    def __init__(self, name, location, description, positive_points, negative_points, like_callback, dislike_callback):
        self.name = name
        self.location = location
        self.description = description
        self.positive_points = positive_points
        self.negative_points = negative_points
        self.like_callback = like_callback
        self.dislike_callback = dislike_callback

    def display(self):
        # Create a card layout with the recommendation details
        card_layout = f"""
        Name: {self.name}
        Location: {self.location}
        Description: {self.description}
        
        Positive Points:
        {self.format_points(self.positive_points)}
        
        Negative Points:
        {self.format_points(self.negative_points)}
        
        [Like] [Dislike]
        """
        return card_layout

    def format_points(self, points):
        return "\n".join(f"- {point}" for point in points)

    def like(self):
        self.like_callback(self)

    def dislike(self):
        self.dislike_callback(self)