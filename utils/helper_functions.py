"""
This module contains helper functions to aid the different functionality of the bot.
"""
import re
from utils.setup import (EXAMPLE_COMMAND, MENTION_REGEX, GREETINGS, slack_client,
                            starterbot_id, Labels, city_name_userid, msg_to_resp)
from utils.api_wrappers import post_message, get_weather_and_location


def classify_message(msg, userid=None):
    """
        Classifies the message into buckets.
    """
    if msg.startswith(EXAMPLE_COMMAND):
        return Labels.example.name
    elif msg.startswith("Welcome"):
        return Labels.greeting.name
    elif re.search(r'(.*) weather|weather in (.*)|(.*)\'s weather ', msg, re.I|re.M):
        return Labels.weather.name
    elif re.search(r'weather', msg, re.I|re.M):
        return Labels.weather_my_loc.name
    else:
        return Labels.default.name

def get_city_name(msg, user_id=None):
    """
        Extract the city name for the message.
    """
    if re.search(r'(.*) weather|weather in (.*)|(.*)\'s weather ', msg, re.I|re.M):
        mtch = re.search(r'(.*) weather|weather in (.*)|(.*)\'s weather ', msg, re.I|re.M)
        city = next((x for x in mtch.groups() if x is not None), None)
            # filter(lambda x: x is not None, mtch.groups()), None)
    else:
        city = city_name_userid.get(user_id, labels.dnt_knw_loc.name)
    return city

def get_weather_in_city(city):
    """
        Get the weather conditions in a given city.
    """
    try:
        w, l = get_weather_and_location(place=city)

        status = w.get_status()
        temp = w.get_temperature(unit='celsius')
        temp_cur = temp.get('temp', 0)
        temp_max = temp.get('temp_max', float('inf'))
        temp_min = temp.get('temp_min', float('-inf'))
        unit = 'Celsius'

        weather = """The weather in {city} is {status}. The current temperature is {cur} {unit} \
and is expected to have a high of {max} {unit} and a \
low of {min} {unit}""".format(city=city, status=status, cur=temp_cur, max=temp_max,
                                  min=temp_min, unit=unit)
    except Exception:
        weather = """I'm sorry; I'm still learning. I'm currently unable to find the weather \
of {city}. May be the city has other names? Have you tried them?""".format(city=city)
    return weather


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:

        if event["type"] == "member_joined_channel" and event["user"] != starterbot_id:
            user_id, channel = event["user"], event["channel"]
            message = "Welcome!!"
            return message, channel, user_id

        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"], user_id
    return None, None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel, user_id=None):
    """
        Executes bot command if the command is known
    """

    msg = classify_message(command)

    # Use the classified message to obtain the corresponding response
    response = msg_to_resp.get(msg, None)

    if msg == Labels.greeting.name:
        response = response.format(user_id=user_id, channel=channel)
    elif msg in [Labels.weather.name, Labels.weather_my_loc.name]:
        city = get_city_name(command, user_id)
        response = get_weather_in_city(city)

    # Sends the response back to the channel
    post_message(msg=response or default_response, channel=channel)
