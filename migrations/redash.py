"""Redash to Metabase migration module."""

from typing import Dict, Any, List
from .base import BaseMigration, QueryType


class RedashMigration(BaseMigration):
    
    def get_card_from_query(self, redash_query: Dict[str, Any], db_id: int, collection_id: int) -> Dict[str, Any]:
        sql_query = redash_query.get("query", "")
        description = redash_query.get("description")
        name = redash_query.get("name")
        query_type = QueryType.SQL.value  # Assuming SQL query type for Redash
        viz_settings = self.extract_viz_settings(redash_query)
        parameters = self.extract_parameters(redash_query)
        template_tags = self.extract_template_tags(redash_query, parameters)

        return {
            "dataset_query": {
                "database": db_id,
                "type": "native",
                query_type: {
                    query_type: sql_query,
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
  
    def extract_parameters(self, redash_query: Dict[str, Any]) -> List[Dict[str, Any]]:
        parameters = []
        redash_params = redash_query.get("options", {}).get("parameters", [])
        for param in redash_params:
            type_ = param.get("type", "text")
            value = param.get("value")
            if type_ in ["text", "number", "date"]:
                mx_parameter = {
                    "id": param.get("name"),
                    "type": type_,
                    "name": param.get("name"),
                    "target": ["variable", ["template-tag", param.get("name", "")]],
                }
                if isinstance(value, str) or isinstance(value, int):
                    mx_parameter['required'] = True
                    mx_parameter['default'] = value
                parameters.append(mx_parameter)
            
            elif (type_ == "date-range"):
                for date_key in ["start", "end"]:
                    param_name = f'{param.get("name")}_{date_key}'
                    mx_parameter = {
                        "id": param_name,
                        "type": "date",
                        "name": param_name,
                        "target": ["variable", ["template-tag", param_name]],
                    }
                    if isinstance(value, dict):
                        mx_parameter['required'] = True
                        mx_parameter['default'] = value.get(date_key)
                    parameters.append(mx_parameter)
        return parameters

    def extract_template_tags(self, redash_query: Dict[str, Any], parameters: List[Dict[str, Any]]) -> Dict[str, Any]:
        template_tags = {}
        for param in parameters:
            template_tags[param["id"]] = {
                "id": param["id"],
                "name": param["name"],
                "type": param["type"],
                "default": param.get("default", None),
                "required": param.get("required", False),
                "display_name": param["name"].replace("_", " ").title()
            }
        return template_tags

    def extract_viz_settings(self, redash_query: Dict[str, Any]) -> Dict[str, Any]:
        viz_settings = {}
        return viz_settings
