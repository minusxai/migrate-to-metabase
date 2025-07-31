"""Base migration class for BI tool to Metabase migrations."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from enum import Enum


class BiTool(Enum):
    REDASH = 'redash'
    LOOKER = 'looker' 
    TABLEAU = 'tableau'


class QueryType(Enum):
    SQL = 'native'
    MBQL = 'query'


class BaseMigration(ABC):
    """Abstract base class for BI tool migrations to Metabase."""
    
    @abstractmethod
    def get_card_from_query(self, query_data: Dict[str, Any], db_id: int, collection_id: int) -> Dict[str, Any]:
        """
        Convert a BI tool query to a Metabase card configuration.
        
        Args:
            query_data: The source BI tool query data
            db_id: The database ID to associate with the Metabase card
            collection_id: The collection ID to place the card in
            
        Returns:
            dict: Metabase card configuration
        """
        pass
    
    @abstractmethod
    def extract_parameters(self, query_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract parameters from the source query data.
        
        Args:
            query_data: The source BI tool query data
            
        Returns:
            list: List of parameter configurations for Metabase
        """
        pass
    
    @abstractmethod
    def extract_template_tags(self, query_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract template tags from the source query data.
        
        Args:
            query_data: The source BI tool query data
            
        Returns:
            dict: Template tags configuration for Metabase
        """
        pass
    
    @abstractmethod
    def extract_viz_settings(self, query_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract visualization settings from the source query data.
        
        Args:
            query_data: The source BI tool query data
            
        Returns:
            dict: Visualization settings for Metabase
        """
        pass