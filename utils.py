from dotenv import load_dotenv
import httpx
import os
from enum import Enum

load_dotenv()

METABASE_API_KEY = os.getenv('METABASE_API_KEY')
assert METABASE_API_KEY, "METABASE_API_KEY environment variable is not set"
METABASE_URL = os.getenv('METABASE_URL')
assert METABASE_URL, "METABASE_URL environment variable is not set"


async def make_api_request(url_path: str, payload: dict = None) -> dict:
    """
    Make an API request and return the response as a dictionary.
    Args:
        url (str): The URL to make the request to.
        payload (dict): The payload to send in the request.
    Returns:
        dict: The JSON response from the API.
    """
    headers = {
        'x-api-key': METABASE_API_KEY,
    }
    url = f"{METABASE_URL}{url_path}"
    # print(f"Making request to {url} with payload: {payload}")
    async with httpx.AsyncClient() as client:
        if payload:
            headers['Content-Type'] = 'application/json'
            response = await client.post(url, json=payload, headers=headers)
        else:
            response = await client.get(url, headers=headers)

        response.raise_for_status()
        return response.json()


class BiTool(Enum):
    REDASH = 'redash'
    LOOKER = 'looker'
    TABLEAU = 'tableau'


class QueryType(Enum):
    SQL = 'native'
    MBQL = 'query'


def get_query_config(db_id: int, query_type: QueryType = 'native', sql: str = None, mbql: dict = None, 
                     viz_settings: dict = {}, parameters: list = [], template_tags: dict = {},
                     name: str='', description: str='', collection_id: int = 1) -> dict:
    """
    Get the query configuration for SQL/MBQL.
    Args:
        db_id (int): The ID of the database to run the query on.
        sql (str): The SQL query to run.
    Returns:
        dict: The query configuration.
    """
    if query_type == QueryType.SQL:
        assert sql is not None, "sql should be provided when query type is sql"
    elif query_type == QueryType.MBQL:
        assert mbql is not None, "mbql should be provided when query type is mbql"

    return {
        "dataset_query": {
            "database": db_id,
            "type": "native",
            QueryType.SQL.value: {
                QueryType.SQL.value: sql,
                "template-tags": template_tags
            }
        },
        "display": "table",
        "parameters": parameters,
        "visualization_settings": viz_settings,
        "type": "question",
        "name": name,
        "description": description,
        "collection_id": collection_id
    }
