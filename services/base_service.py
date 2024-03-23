from abc import ABC, abstractmethod
from typing import Any, Optional

from utils.logger import setup_logger
from utils.environment import EnvironmentManager
from config import *

class BaseAIService(ABC):
    """Base class for all AI services with common functionality."""
    
    def __init__(self):
        self.logger = setup_logger(self.__class__.__name__)
        
    @abstractmethod
    def process(self, query: str) -> Any:
        """Process the user query and return appropriate response."""
        pass
    
    def handle_error(self, error: Exception, context: Optional[str] = None) -> None:
        """Standardized error handling across services."""
        error_msg = f"{error.__class__.__name__}: {str(error)}"
        if context:
            error_msg = f"{context} - {error_msg}"
        self.logger.error(error_msg)
        
    def validate_api_keys(self) -> bool:
        """Validate that required API keys are present."""
        required_keys = self._get_required_api_keys()
        if not EnvironmentManager.validate_api_keys(required_keys):
            self.logger.error(f"Missing required API keys: {', '.join(required_keys)}")
            return False
        return True
    
    @abstractmethod
    def _get_required_api_keys(self) -> list[str]:
        """Return list of required API keys for the service."""
        pass