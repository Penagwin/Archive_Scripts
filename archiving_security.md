[8/20/21]

So we want to backup every Defcon video from youtube.
Their url/playlist is "https://www.youtube.com/user/DEFCONConference/videos"
We'll use `youtube-dl` and `jq`.


So my first attempt was to use just the basic function of youtube-dl by just giving it the DEFCON playlist.
```bash
youtube-dl -f best --write-description --write-info "https://www.youtube.com/user/DEFCONConference/videos" 
```
However this would take forever as it's only one video at a time, and later we'll learn there's 3394 videos. 
On top of that, videos using DASH as well as youtube rate limits can mean you're downloading at a measly 66kbps.
To solve this problem, we're going to grab a list of all the video urls, and distrube them among several `youtube-dl` instances. 
At this point in my research I found https://alexwlchan.net/2020/07/how-to-do-parallel-downloads-with-youtube-dl/ who used xargs as a elagent way to do this.
I'm going to be saving the urls to a file though for faster start times, and for better interopability with other tools.


Downloading a list of all the urls from their channel.

```bash
# Thank you https://stackoverflow.com/a/65440501
youtube-dl -j --flat-playlist "https://www.youtube.com/user/DEFCONConference/videos" | jq -r '.id' | sed 's_^_https://youtu.be/_' > videoList.txt

# Let's checkout `videoList.txt`
wc -l videoList.txt
# 3394 videoList.txt

head -n 3 videoList.txt
# https://youtu.be/9_fJv_weLU0
# https://youtu.be/XuNqM-0Ufx0
# https://youtu.be/TWcBySQgfBE
```

```bash
# Modified from https://alexwlchan.net/2020/07/how-to-do-parallel-downloads-with-youtube-dl/
cat videoListPart.txt.aa | xargs -I '{}' -P 2 youtube-dl --proxy socks5://ca10-wg.socks5.mullvad.net:1080 -f bestvideo+bestaudio --write-description --write-info '{}'
cat videoListPart.txt.ab | xargs -I '{}' -P 2 youtube-dl --proxy socks5://us91-wg.socks5.mullvad.net:1080 -f bestvideo+bestaudio --write-description --write-info '{}'
cat videoListPart.txt.ac | xargs -I '{}' -P 2 youtube-dl --proxy socks5://us92-wg.socks5.mullvad.net:1080 -f bestvideo+bestaudio --write-description --write-info '{}'
cat videoListPart.txt.ad | xargs -I '{}' -P 2 youtube-dl --proxy socks5://us93-wg.socks5.mullvad.net:1080 -f bestvideo+bestaudio --write-description --write-info '{}'
cat videoListPart.txt.ae | xargs -I '{}' -P 2 youtube-dl --proxy socks5://us94-wg.socks5.mullvad.net:1080 -f bestvideo+bestaudio --write-description --write-info '{}'
cat videoListPart.txt.af | xargs -I '{}' -P 2 youtube-dl --proxy socks5://us95-wg.socks5.mullvad.net:1080 -f bestvideo+bestaudio --write-description --write-info '{}'
cat videoListPart.txt.ag | xargs -I '{}' -P 2 youtube-dl --proxy socks5://us96-wg.socks5.mullvad.net:1080 -f bestvideo+bestaudio --write-description --write-info '{}'
cat videoListPart.txt.ah | xargs -I '{}' -P 2 youtube-dl --proxy socks5://us97-wg.socks5.mullvad.net:1080 -f bestvideo+bestaudio --write-description --write-info '{}'
youtube-dl --proxy socks5://us70-wg.socks5.mullvad.net:1080 -f bestvideo+bestaudio --write-description --write-info 'https://www.youtube.com/c/Bisqwit/videos'
youtube-dl --proxy socks5://us71-wg.socks5.mullvad.net:1080 -f bestvideo+bestaudio --write-description --write-info 'https://www.youtube.com/c/PwnFunction/videos'
youtube-dl --proxy socks5://us71-wg.socks5.mullvad.net:1080 -f bestvideo+bestaudio --write-description --write-info 'https://www.youtube.com/c/PwnFunction/videos'

```




```bash
youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' --write-description  "https://www.youtube.com/watch?v=SC8vX0V2ypo" 
youtube-dl -f best --write-description --write-info "https://www.youtube.com/user/DEFCONConference/videos" 
youtube-dl -f best --proxy socks5://ca10-wg.socks5.mullvad.net:1080 --write-description --write-info "https://www.youtube.com/user/DEFCONConference/videos" 
youtube-dl -f best --write-description --write-info "https://www.youtube.com/user/DEFCONConference/videos" 

youtube-dl -j --flat-playlist "https://www.youtube.com/user/" | jq -r '.id' | sed 's_^_https://youtu.be/_' > videoList.txt


youtube-dl --get-id "https://www.youtube.com/user/DEFCONConference/videos" | xargs -I '{}' -P 5 youtube-dl -f best --write-description --write-info 'https://youtube.com/watch?v={}'
```