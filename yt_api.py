import requests
from technical import YT_API
from bs4 import BeautifulSoup


def get_yt_url(request, id: int):

    response = requests.get(f"https://www.googleapis.com/youtube/v3/search?key={YT_API}&q={request}&maxResults={id + 1}")
    try:
        return f"https://www.youtube.com/watch?v={response.json()['items'][id]['id']['videoId']}"
    except KeyError:
        response = requests.get(f"https://www.googleapis.com/youtube/v3/channels?"
               f"id={response.json()['items'][id]['id']['channelId']}&part=snippet&key={YT_API}")
        return f"https://www.youtube.com/{response.json()['items'][0]['snippet']['customUrl']}"

def get_song_name(request):
    r = requests.get(request)
    soup = BeautifulSoup(r.text, features="html.parser")
    link = soup.find_all(name="title")[0]
    title = link.text[:-10]

    return title


