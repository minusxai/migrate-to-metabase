# Migrate to Metabase

Migrate queries from various BI tools to Metabase. Once on Metabase, [MinusX](https://minusx.ai) can make analytics 10x faster, more accessible, and fun!

## Supported Tools
- ✅ Redash
- 🚧 Tableau (planned)

## Assets Supported
- ✅ Queries (w/ parameters, template tags)
- 🚧 Dashboards (planned)
- 🚧 Visualizations (planned)


## Setup

Create `.env`:
```
METABASE_API_KEY=your_api_key
METABASE_URL=https://your-metabase.com
```

## Downloading data
This depends on the BI tool you're migrating from. For redash, all queries can be obtained from `/api/queries/<id>`. So the `queries.json` is a list of all the json responses. I'll make a script for this too.


## Usage

```bash
# run with uv
uv run main.py -s redash -f queries.json -d DATABASE_ID -c COLLECTION_ID
```


## Adding New Tools

1. Create class extending `BaseMigration` in `migrations/`
2. Add to `BiTool` enum
3. Update `get_migration_module()` in `main.py`
