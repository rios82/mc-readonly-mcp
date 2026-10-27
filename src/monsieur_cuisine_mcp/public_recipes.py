"""Read-only adapter for observed public Monsieur Cuisine API routes."""
from __future__ import annotations

from typing import Any
import httpx

from .config import API_BASE_URL, DEFAULT_LANGUAGE, REQUEST_TIMEOUT_SECONDS

class PublicRecipeAPIError(RuntimeError):
    pass

async def _get(path: str, params: dict[str, Any] | None = None, language: str = DEFAULT_LANGUAGE) -> Any:
    # Fixed host + relative path only: caller-supplied URLs are never accepted.
    url = f"{API_BASE_URL}/{path.lstrip('/')}"
    headers = {"Accept": "application/json", "Accept-Language": language}
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS, follow_redirects=False) as client:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise PublicRecipeAPIError(f"Public Monsieur Cuisine API request failed: {exc}") from exc

async def search_recipes(query: str, page: int = 1, size: int = 10, language: str = DEFAULT_LANGUAGE) -> Any:
    """Search public recipes. Page starts at 1."""
    page = max(1, int(page))
    # Route and parameters validated against the live public API (same as SmartChef fallback).
    return await _get(
        f"api/v1/recipes/search/page/{page}",
        {
            "q": query,
            "sortBy[0][field]": "lastUpdated",
            "sortBy[0][direction]": "DESC",
        },
        language,
    )

async def list_recipe_filters(language: str = DEFAULT_LANGUAGE) -> Any:
    """Return public filter options, if the upstream service exposes them."""
    # This route is not part of a stable official API; failure is reported clearly.
    return await _get("api/v1/recipes/filters", {"lang": language})

async def get_recipe(recipe_id: str, language: str = DEFAULT_LANGUAGE) -> Any:
    """Get a public recipe by ID. Only numeric IDs are accepted."""
    recipe_id = str(recipe_id).strip()
    if not recipe_id.isdigit():
        raise ValueError("recipe_id must contain digits only")
    return await _get(f"api/v2/recipes/{recipe_id}", {"lang": language})
