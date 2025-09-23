from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from langchain.tools import BaseTool
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()


class CryptoBaseTool(BaseTool, ABC):
    """Base class for all crypto analysis tools"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._validate_api_key()

    @abstractmethod
    def _validate_api_key(self) -> None:
        """Validate that required API key is present"""
        pass

    @abstractmethod
    def _make_request(self, **kwargs) -> Dict[str, Any]:
        """Make API request and return response"""
        pass

    def _handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """Handle API errors consistently"""
        return {
            "error": str(error),
            "context": context,
            "success": False
        }