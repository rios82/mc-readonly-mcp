
import os

API_BASE_URL = os.getenv("MC_API_BASE_URL", "https://mc-api.tecpal.com").rstrip("/")
MCP_BEARER_TOKEN = os.getenv("MCP_BEARER_TOKEN", "")
PORT = int(os.getenv("PORT", "8000"))
DEFAULT_LANGUAGE = os.getenv("MC_LANGUAGE", "en-US")
REQUEST_TIMEOUT_SECONDS = float(os.getenv("MC_REQUEST_TIMEOUT_SECONDS", "15"))
