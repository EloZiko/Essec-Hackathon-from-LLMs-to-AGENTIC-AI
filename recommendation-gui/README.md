# Recommendation Generator GUI

This project is a graphical user interface (GUI) for a recommendation generator that allows users to input their preferences and receive personalized recommendations. The application integrates various components to facilitate user interaction, display recommendations, and manage user feedback through a swipe feature.

## Project Structure

The project is organized into several directories and files, each serving a specific purpose:

- **src/**: Contains the main application code.
  - **app.py**: The main entry point of the GUI application.
  - **components/**: Contains UI components for the application.
    - **recommendation_card.py**: Defines the RecommendationCard class for displaying individual recommendations.
    - **search_panel.py**: Provides the user interface for inputting search queries.
    - **results_panel.py**: Displays the results of the recommendations.
  - **controllers/**: Contains the logic for handling user input and updating the GUI.
    - **recommendation_controller.py**: Manages the recommendation generation process.
  - **assets/**: Contains style definitions for the GUI components.
    - **styles.py**: Defines layout and appearance settings.
  - **utils/**: Contains utility functions for various tasks.
    - **helpers.py**: Assists with data formatting and validation.

- **core/**: Contains the core logic of the application.
  - **llm_service.py**: Interacts with the LLM API to generate recommendations.
  - **recommendation.py**: Defines the Recommendation class for managing recommendation data.

- **config/**: Contains configuration settings for the application.
  - **settings.py**: Stores API keys and default values.

- **utils/**: Contains additional utility functions.
  - **formatters.py**: Functions for formatting recommendation outputs.

- **.env**: Contains environment variables for configuration.

- **requirements.txt**: Lists the dependencies required for the project.

## Setup Instructions

1. **Clone the Repository**: 
   ```
   git clone <repository-url>
   cd recommendation-gui
   ```

2. **Install Dependencies**: 
   Ensure you have Python installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**: 
   Create a `.env` file in the root directory and add your API keys and other necessary configurations.

4. **Run the Application**: 
   Execute the following command to start the GUI:
   ```
   python src/app.py
   ```

## Usage Guidelines

- Upon launching the application, users can input their preferences in the search panel.
- The application will generate recommendations based on the input and display them in the results panel.
- Users can swipe left to dislike or right to like recommendations, which will be reflected in the displayed results.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.