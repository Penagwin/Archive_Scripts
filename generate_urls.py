
import argparse
import os
import random

import googleapiclient.discovery
import requests
from dotenv import load_dotenv

load_dotenv()


youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = os.environ.get("YOUTUBE_API_KEY"))

request = channels_response = youtube.channels().list(
        forUsername="blackhatofficialyt",
        part="id, snippet, statistics, contentDetails, topicDetails"
).execute()

print(request)
request = youtube.playlistItems().list(
    part = "snippet",
    playlistId = "UUJ6q9Ie29ajGqKApbLqfBOg",#request['items'][0]['id'],
    maxResults = 50
)

playlists = []


while request is not None:
    response = request.execute()
    playlists += response["items"]
    request = youtube.playlists().list_next(request, response)

# Get each video from the playlist
for video in playlists:
	print(video['snippet']['resourceId']['videoId'])
print(f"total: {len(playlists)}")
#print(playlists)
print(len(playlists))

# URL for Mullvad's json API
MULLVAD_SERVER_API_URL = 'https://api.mullvad.net/www/relays/all/'

# Base folder for downloads
STORAGE_DIR =  "/run/media/penagwin/easystore/defcon/"
SOCKS5_SERVER_LIST = []
SOCKS_COUNTRY_WHITELIST = ["us", "ca"]
SOCKS_CITY_BLACKLIST = []

# Channels we can grab from
# @TODO allow us to specify a channel and it's location manually
CHANNELS = [
    "bisqwit",
    "pwnfunction",
    "shakaconitconference",
    "blackhatofficialyt",
    "ippsec",
    "troyhuntdotcom",
    "webpwnized",    
    "defconconference",
    "stacksmashing",
    "wildwesthackinfest",    
    "webpwnized",
]

# Grab the available SOCKS5 proxies from Mullvad
resp = requests.get(url=MULLVAD_SERVER_API_URL)
data = resp.json() 

# Go through each of the servers and filter out the ones we need
for server in data:
    if server.get("country_code") in SOCKS_COUNTRY_WHITELIST and server.get("city_code") not in SOCKS_CITY_BLACKLIST:
        socks_name = server.get("socks_name")
        if socks_name != None:
            SOCKS5_SERVER_LIST.append(f"socks5://{socks_name}.mullvad.net:1080")


# Setup Argparse
parser = argparse.ArgumentParser()

parser.add_argument("channel", help="channel name to get")
parser.add_argument("--parallel", default=2, type=int, help="Number of parrelel youtube-dl processes per proxy")

args = parser.parse_args()

# Clean and validate the inputs
selected_channel = args.channel.lower()
parallel_threads = int(args.parallel)

if selected_channel not in CHANNELS:
    print("ERROR: You must specify one of these channels:")
    print(", ".join(CHANNELS))


# Print all the combinations for testing
for selected_channel in CHANNELS:
    selected_socks_proxy = random.choice(SOCKS5_SERVER_LIST)

    print(f'cd {STORAGE_DIR}{selected_channel} && youtube-dl --get-id "https://www.youtube.com/{selected_channel}/videos" | xargs -I "{{}}" -P {parallel_threads} youtube-dl --proxy {selected_socks_proxy} -f bestvideo+bestaudio --write-description --write-info "{{}}" ')
