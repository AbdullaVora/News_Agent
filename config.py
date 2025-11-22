"""
Config loader for Smart News Aggregator
Loads API keys from .env file securely
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_AI_STUDIO_KEY = GOOGLE_API_KEY  # alias for compatibility

    @staticmethod
    def validate():
        if not Config.GOOGLE_API_KEY:
            raise ValueError("❌ Missing GOOGLE_API_KEY in .env file!")
        print("🔑 API Key loaded successfully!")
