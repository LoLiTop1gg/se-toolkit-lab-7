import os
from pathlib import Path
from dotenv import load_dotenv

# Path to .env.bot.secret (in project root, one level up from bot/)
ENV_FILE = Path(__file__).parent.parent / ".env.bot.secret"

# Load environment variables from .env.bot.secret
load_dotenv(ENV_FILE)

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# LMS Backend configuration
LMS_API_URL = os.getenv("LMS_API_URL", "http://localhost:42002")
LMS_API_KEY = os.getenv("LMS_API_KEY", "")

# LLM configuration
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_API_BASE_URL = os.getenv("LLM_API_BASE_URL", "http://localhost:42005/v1")
LLM_API_MODEL = os.getenv("LLM_API_MODEL", "coder-model")
