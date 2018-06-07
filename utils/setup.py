"""
This module contains all the constants used.
"""
from config import SLACK_BOT_TOKEN
from slackclient import SlackClient

# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# instantiate Slack client
slack_client = SlackClient(SLACK_BOT_TOKEN)

# Read bot's user ID by calling Web API method `auth.test`
starterbot_id = slack_client.api_call("auth.test")["user_id"]

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
GREETINGS = "Welcome"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"