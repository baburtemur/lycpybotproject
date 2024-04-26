import discord
import requests
import technical
import datetime as dt
import json


def pisun():
    dt_string_s = "2024-05-01T15:20:15"
    dt_string_e = "2024-05-01T17:20:15"

    auth_headers = {
        "Authorization": f"Bot {technical.TOKEN}",
        "User-Agent": f"DiscordBot ({technical.BOT_AUTH_HEADER}) Python/3.8 aiohttp/3.9.5",
        "Content-Type": "application/json"
    }
    event_create_url = f"https://discord.com/api/v9/guilds/{1231344759487070249}/scheduled-events"
    event_name = "abcd"
    event_description = "abc"
    event_start_time = dt_string_s
    event_end_time = dt_string_e
    event_metadata = {'location': 'Developer server'}
    ff = {
        'name': event_name,
        'privacy_level': 2,
        'scheduled_start_time': event_start_time,
        'scheduled_end_time': event_end_time,
        'description': event_description,
        'channel_id': None,
        'entity_metadata': event_metadata,
        'entity_type': 3
    }
    event_data = json.dumps(ff)
    response = requests.post(event_create_url, headers=auth_headers, data=event_data)
    print(response.text)
    print(response.status_code)
    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print("Failed to send the message.")
        print(response.text)

token = technical.TOKEN
channel_id = 1231344759935602774
message = "Hey, How are you?"

#message_post(token, channel_id, message)
pisun()