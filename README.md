# Monsieur Cuisine Read-only MCP

Unofficial, read-only MCP server exposing public Monsieur Cuisine recipe lookup tools.
It does not log in to Lidl, store cookies, access personal recipes, change favorites, or create/edit/delete/publish recipes.

## Tools
- `search_recipes`: search the public recipe catalogue.
- `list_recipe_filters`: retrieve public filter options.
- `get_recipe`: retrieve public recipe details by ID.

## Run locally
Python 3.11+ recommended.

```bash
python -m venv .venv
# Linux/macOS:
. .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m src.monsieur_cuisine_mcp.readonly_remote
```

The service listens on `0.0.0.0:$PORT` (default 8000), MCP endpoint `/mcp`, health endpoint `/healthz`.

## Render
Create a new Web Service from this repository. Render can use the included `Dockerfile` and `render.yaml`.
Set `MCP_BEARER_TOKEN` to a long random secret in Render's Environment settings. Do not commit the token.
The health endpoint is public; all MCP requests require `Authorization: Bearer <MCP_BEARER_TOKEN>`.

## API caveat
Monsieur Cuisine does not publish a stable official public API contract. The server uses observed public endpoints at `mc-api.tecpal.com`; they may change. This reconstructed package has not been validated against the live upstream API. Test it before integrating it into SmartChef MC.

## Disclaimer
Unofficial and not affiliated with Lidl, Monsieur Cuisine, or TecPal. Respect the service terms, rate limits, copyright and recipe rights.
