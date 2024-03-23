"""Module for centralized environment variable management."""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class EnvironmentManager:
    """Manages access to environment variables and API keys."""
    
    @staticmethod
    def get_api_key(key_name: str) -> Optional[str]:
        """Get an API key from environment variables.
        
        Args:
            key_name: Name of the API key environment variable
            
        Returns:
            The API key value if found, None otherwise
        """
        return os.getenv(key_name)
    
    @staticmethod
    def validate_api_keys(required_keys: list[str]) -> bool:
        """Validate that all required API keys are present.
        
        Args:
            required_keys: List of required API key names
            
        Returns:
            True if all required keys are present, False otherwise
        """
        for key in required_keys:
            if not os.getenv(key):
                return False
        return True