import os
import logging
from dotenv import load_dotenv

# Configure logging
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'service_logs.log'),
    level=logging.INFO,
    format='%(filename)s - %(funcName)s - %(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

try:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")
    
    if not OPENAI_API_KEY or not SLACK_BOT_TOKEN or not SLACK_CHANNEL:
        raise ValueError("Missing environment variables")

    logger.info("Environment variables loaded successfully")

except Exception as e:
    logger.error(f"Error loading environment variables: {e}")
    raise
