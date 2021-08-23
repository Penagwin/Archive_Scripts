import argparse
import os

from dotenv import load_dotenv

load_dotenv()

# Setup Argparse
parser = argparse.ArgumentParser()

parser.add_argument("username", help="channel username to get")
parser.add_argument("--method", default="api", choices=["api", "dl"], help="Number of parrelel youtube-dl processes per proxy")
parser.add_argument("--print-stats", default=False, action="store_true", help="Print stats")
parser.add_argument("--no-data", default=False, action="store_true", help="Skip printing data")
parser.add_argument("--token", default="", type=str, help="Youtube API Token")
parser.add_argument("--data-type", choices=["raw_json", "id_only", "url_only"], default="url_only", help="Data type to use")
args = parser.parse_args()

# Clean and validate the inputs
grab_method = args.method
selected_channel = args.username.lower()
no_data = args.no_data
print_stats = args.print_stats
data_type = args.data_type
token = args.token


if grab_method == "api":
    
    # Figure out the YOUTUBE 
    YOUTUBE_API_TOKEN = os.environ.get('YOUTUBE_API_TOKEN', "")

    if YOUTUBE_API_TOKEN == "":
        YOUTUBE_API_TOKEN = token

    if len(YOUTUBE_API_TOKEN) < 8 :
        raise Exception("Youtube API Key is required when using the api method.")
    
    import googleapiclient.discovery
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_TOKEN)

    if selected_channel == "":
        print("ERROR: You must specify a channel.")

    # Grab the channel information so we can get the ID of the uploads playlist
    request = channels_response = youtube.channels().list(forUsername=selected_channel, part="id, snippet, statistics, contentDetails, topicDetails").execute()

    # Grab the initial videos from the uploads playlist
    request = youtube.playlistItems().list(part = "snippet", playlistId = request['items'][0]['contentDetails']['relatedPlaylists']['uploads'], maxResults = 50)


    # Add each video to the playlist and download the next page of videos
    playlists = []    
    while request is not None:
        response = request.execute()
        playlists += response["items"]
        request = youtube.playlists().list_next(request, response)

    # Output the data as specified by the user
    if not no_data:
        if data_type == "raw_json":
            print(playlists)
        elif data_type == "url_only":
            for video in playlists:
                print(f"https://www.youtube.com/watch?v={video['snippet']['resourceId']['videoId']}")
        elif data_type == "id_only":
            for video in playlists:
                print(video['snippet']['resourceId']['videoId'])

    # @TODO Add statistics that can be displayed 
    if print_stats:
            print(f"total: {len(playlists)}")
