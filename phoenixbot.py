"""
This is the initial module for the slack bot.
"""
import os
import time
from utils.setup import RTM_READ_DELAY, slack_client, starterbot_id
from utils.helper_functions import parse_bot_commands, handle_command

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")

        while True:
            command, channel, user_id = parse_bot_commands(slack_events=slack_client.rtm_read())
            if command:
                handle_command(command, channel, user_id)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
