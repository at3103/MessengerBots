"""
This module contains helper functions to aid the different functionality of the bot.
"""
import re
from utils.setup import EXAMPLE_COMMAND, MENTION_REGEX, GREETINGS, slack_client, starterbot_id
from utils.api_wrappers import post_message

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:

        if event["type"] == "member_joined_channel" and event["user"] != starterbot_id:
            user_id, channel = event["user"], event["channel"]
            message = "Welcome <@{user_id}> to the channel <#{channel}>\
            ! Hope you have a good time here!".format(user_id=user_id, channel=channel)
            return message, channel

        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None

    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    elif command.startswith(GREETINGS):
        response = command

    # Sends the response back to the channel
    post_message(msg=response or default_response, channel=channel)