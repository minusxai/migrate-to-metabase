import argparse
import json
from dotenv import load_dotenv
from utils import BiTool, make_api_request

load_dotenv()


def get_migration_module(bi_tool: BiTool):
    """Import and return the appropriate migration module."""
    if bi_tool == BiTool.REDASH:
        import migrations.redash as redash
        return redash
    elif bi_tool == BiTool.LOOKER:
        raise NotImplementedError("Looker migration not implemented yet")
    elif bi_tool == BiTool.TABLEAU:
        raise NotImplementedError("Tableau migration not implemented yet")
    else:
        raise ValueError(f"Unsupported BI tool: {bi_tool}")


async def main():
    parser = argparse.ArgumentParser(description="Migrate BI tool queries to Metabase")
    parser.add_argument(
        "-s",
        "--source", 
        type=str, 
        choices=[tool.value for tool in BiTool],
        required=True,
        help="Source BI tool to migrate from"
    )
    parser.add_argument(
        "-f",
        "--data-file",
        type=str,
        required=True,
        help="Path to the data file with queries to migrate"
    )
    parser.add_argument(
        "-d",
        "--db-id",
        type=int,
        required=True,
        help="Database ID to associate with the Metabase card"
    )
    parser.add_argument(
        "-c",
        "--collection-id",
        type=int,
        default=1,
        help="Collection ID to place the Metabase card in (default: 1)"
    )
    
    args = parser.parse_args()
    source_tool = BiTool(args.source)
    
    # Load queries data
    with open(args.data_file) as f:
        queries_data = json.load(f)
    
    # Get migration module
    migration_module = get_migration_module(source_tool)
    
    # Process queries
    for query_data in queries_data:
        card_config = migration_module.get_card_from_query(query_data, args.db_id, args.collection_id)
        response = await make_api_request(
            url_path="/api/card",
            payload=card_config
        )
        print(f"Created card: {response}")
        break


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
