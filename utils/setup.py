"""
This module contains all the constants used.
"""
import pyowm
from slackclient import SlackClient
from config import SLACK_BOT_TOKEN, OWM_API_KEY
from enum import Enum

# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# instantiate Slack client
slack_client = SlackClient(SLACK_BOT_TOKEN)

# Read bot's user ID by calling Web API method `auth.test`
starterbot_id = slack_client.api_call("auth.test")["user_id"]

owm = pyowm.OWM(OWM_API_KEY)

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
NOT_IMPLEMENTED = "Sure...write some more code then I can do that!"
GREETINGS = "Welcome <@{user_id}> to the channel <#{channel}>! Hope you have a good time here!"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
WEATHER_REGEX = "*weather*"


msg_to_resp = {"example":NOT_IMPLEMENTED,
               "greeting":GREETINGS,
               "default":"Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)}

city_name_userid = dict()

class Labels(Enum):
    """
    Enum for the different type of commands for the slack bot.
    """

    example = "example"
    greeting = "greeting"
    default = "default"
    weather = "weather in city"
    weather_my_loc = "weather in my location"
    dnt_knw_loc = "My Apologies! I don't have the capability to guess your current location yet!\
     I'm still learning. Please tell me your city, I'll remember it the next time. Trust me!"