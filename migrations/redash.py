"""Redash to Metabase migration module."""

from typing import Dict, Any, List
from utils import get_query_config, QueryType


def get_card_from_query(redash_query: Dict[str, Any], db_id: int, collection_id: int) -> Dict[str, Any]:
    """
    Convert a Redash query to a Metabase card configuration.
    
    Args:
        redash_query: The Redash query data containing query info
        db_id: The database ID to associate with the Metabase card

    Returns:
        dict: Metabase card configuration
    """
    # Extract basic query information
    sql_query = redash_query.get("query", "")
    description = redash_query.get("description")
    name = redash_query.get("name")
    

    query_config = get_query_config(
        db_id=db_id,
        query_type=QueryType.SQL,
        sql=sql_query,
        parameters=extract_parameters(redash_query),
        template_tags=extract_template_tags(sql_query),
        viz_settings=extract_viz_settings(redash_query),
        name=name,
        description=description,
        collection_id=collection_id
    )

    return query_config


def extract_parameters(redash_query: Dict[str, Any]) -> List[Dict[str, Any]]:
    parameters = []
    return parameters


def extract_template_tags(redash_query: Dict[str, Any]) -> Dict[str, Any]:
    template_tags = {}
    return template_tags


def extract_viz_settings(redash_query: Dict[str, Any]) -> Dict[str, Any]:
    viz_settings = {}
    return viz_settings

