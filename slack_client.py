import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config import SLACK_BOT_TOKEN, SLACK_CHANNEL
import os

# Configure logging
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'service_logs.log'),
    level=logging.INFO,
    format='%(filename)s - %(funcName)s - %(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

client = WebClient(token=SLACK_BOT_TOKEN)

def post_to_slack(message: str):
    """
    Post a message to a Slack channel.

    Args:
        message (str): The message to post to Slack.

    Returns:
        dict: The response from the Slack API.
    """
    try:
        response = client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        logger.info(f"Message posted to Slack: {message}")
        return response
    except SlackApiError as e:
        logger.error(f"Error posting to Slack: {e.response['error']}")
        raise
