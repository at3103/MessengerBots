"""
This module includes the wrappers written for the slack APIs from SlackClient library.abs

Author: Ashwin Karthik Tamilselvan
"""
from utils.setup import slack_client, owm

def post_message(msg, channel, timestamp=None, user=None):
    """
    This method acts as a wrapper around the postMessage and postEmphemeral APIs.
    """
    if user:
        return slack_client.api_call("chat.postEphemeral", channel=channel
                                     , text=msg, user=user)
    else:
        return slack_client.api_call("chat.postMessage", channel=channel
                                     , text=msg, thread_ts=timestamp)

def update_message(msg, channel, timestamp):
    """
    This method acts as a wrapper around the update message API.
    """
    return slack_client.api_call("chat.update", channel=channel
                                 , text=msg, ts=timestamp)

def delete_message(msg, channel, timestamp):
    """
    This method acts as a wrapper around the delete message API.
    """
    return slack_client.api_call("chat.delete", channel=channel
                                 , ts=timestamp)

def add_reaction(emoji, channel, timestamp):
    """
    This method acts as a wrapper around the add reaction API.
    """
    return slack_client.api_call("reactions.add", channel=channel,
                                 name=emoji, timestamp=timestamp)

def remove_reaction(emoji, channel, timestamp):
    """
    This method acts as a wrapper around the remove reaction API.
    """
    return slack_client.api_call("reactions.remove", channel=channel,
                                 name=emoji, timestamp=timestamp)

# API Wrappers for OWM

def get_weather_and_location(place=None, cityid=None, coords=None, zipcode=None):
    """
    Extract the weather and location object for a given location attribute.
    """
    if cityid:
        o = owm.weather_at_id(cityid)
    elif coords:
        o = owm.weather_at_coords(coords) 
    elif zipcode:
        o = owm.weather_at_zip_code(zipcode)
    else:
        o = owm.weather_at_place(place)

    return o.get_weather(), o.get_location()