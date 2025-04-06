"""
Configuration settings for the recommendation GUI application
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration settings
API_KEY = os.getenv("API_KEY", "your_default_api_key_here")
DEFAULT_LOCATION = os.getenv("DEFAULT_LOCATION", "Paris")
DEFAULT_OUTPUT_FORMAT = "json"
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 2000))
"""