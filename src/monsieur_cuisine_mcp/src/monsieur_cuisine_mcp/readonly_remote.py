
import uvicorn
from .config import PORT, MCP_BEARER_TOKEN
from .readonly_server import create_app

if __name__ == "__main__":
    if not MCP_BEARER_TOKEN:
        raise SystemExit("MCP_BEARER_TOKEN is required; configure it in the hosting provider's secret environment settings.")
    uvicorn.run(create_app(), host="0.0.0.0", port=PORT, log_level="info")
