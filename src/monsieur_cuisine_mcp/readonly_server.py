from __future__ import annotations

import hmac
import json

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from .config import MCP_BEARER_TOKEN
from .public_recipes import (
    search_recipes as api_search,
    list_recipe_filters as api_filters,
    get_recipe as api_get,
)

mcp = FastMCP("monsieur-cuisine-readonly")


@mcp.custom_route("/healthz", methods=["GET"], include_in_schema=False)
async def healthz(request: Request):
    return JSONResponse({
        "status": "ok",
        "service": "mc-readonly-mcp",
    })


@mcp.tool()
async def search_recipes(
    query: str,
    page: int = 1,
    size: int = 10,
    language: str = "en-US",
) -> str:
    """Search the public Monsieur Cuisine recipe catalogue."""
    data = await api_search(
        query=query,
        page=page,
        size=size,
        language=language,
    )
    return json.dumps(data, ensure_ascii=False)


@mcp.tool()
async def list_recipe_filters(language: str = "en-US") -> str:
    """List public recipe filter options."""
    data = await api_filters(language=language)
    return json.dumps(data, ensure_ascii=False)


@mcp.tool()
async def get_recipe(
    recipe_id: str,
    language: str = "en-US",
) -> str:
    """Fetch public recipe details by recipe ID."""
    data = await api_get(
        recipe_id=recipe_id,
        language=language,
    )
    return json.dumps(data, ensure_ascii=False)


class BearerGuard:
    """Require a bearer token for MCP HTTP requests."""

    def __init__(self, app, token: str):
        self.app = app
        self.token = token

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope.get("path", "")

            # Health checks are public; protect the MCP endpoint.
            if path == "/mcp" or path.startswith("/mcp/"):
                headers = {
                    key.lower(): value
                    for key, value in scope.get("headers", [])
                }
                auth = headers.get(
                    b"authorization", b""
                ).decode("latin1")

                scheme, _, supplied = auth.partition(" ")

                if (
                    scheme.lower() != "bearer"
                    or not supplied
                    or not self.token
                    or not hmac.compare_digest(supplied, self.token)
                ):
                    response = JSONResponse(
                        {"error": "Unauthorized"},
                        status_code=401,
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                    await response(scope, receive, send)
                    return

        await self.app(scope, receive, send)


def create_app():
    """Create the protected Streamable HTTP MCP application."""
    app = mcp.http_app(path="/mcp")
    return BearerGuard(app, MCP_BEARER_TOKEN)
