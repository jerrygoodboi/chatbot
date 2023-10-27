from ytmusicapi import YTMusic
from pytube import YouTube
import vlc
def urlfind(text):
    yt = YTMusic()
    search_results = yt.search(text,filter='songs')
    first_result = search_results[0]
    return "music.youtube.com/watch?v="+first_result['videoId']
def mus(text):
    video_url = urlfind(text)
    print(video_url)
    yt = YouTube(video_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_url = audio_stream.url
    instance = vlc.Instance()
    media = instance.media_new(audio_url)
    player = instance.media_player_new()
    player.set_media(media)
    player.play()
    while True:
            state = player.get_state()
            if state == vlc.State.Ended or state == vlc.State.Error:
                    break
file_path = "play.txt"
with open(file_path, "r") as file:
    line = file.readline()
    while line:
        mus(line)
        line = file.readline()
