import speech_recognition as sr
import os
import requests 
import datetime
import elevenlabs
from pytube import YouTube
import vlc
from youtubesearchpython import VideosSearch
#
recognizer = sr.Recognizer()
url = 'http://api.brainshop.ai/get?bid=178546&key=gCppj0KnUpICcFI1&uid=Eldhose&msg='
elevenlabs.set_api_key("fbaab3584cf611c03ebc321df93e0824")
#
def mus(text):
    videos_search = VideosSearch(text, limit = 1)
    results = videos_search.result()
    if 'result' in results:
       first_video = results['result'][0]
       video_url = first_video['link']
       print("URL of the first video:", video_url)
    else:
       print("No results found")
    yt = YouTube(video_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_url = audio_stream.url
    instance = vlc.Instance()
    media = instance.media_new(audio_url)
    player = instance.media_player_new()
    player.set_media(media)
    player.play()
    while True:
        text = rec(3)
        if "stop" in text:
            player.stop()
            break
#
def send_message(input_text):
    response = requests.get(url + input_text)
    data = response.json()
    return data['cnt']
def audio_gen(text):
        audio = elevenlabs.generate(
                text,
                voice = "Glinda"
                 )
        elevenlabs.save(audio, "output.mp3")
        os.system("mplayer output.mp3 2&> /dev/null")
def time():
    current_time = datetime.datetime.now()
    return current_time.strftime('%Y-%m-%d %H:%M:%S')
def rec(val):
    os.system(f"arecord -d {val} -f S16_LE -c 1 -r 44100 -t wav audio.wav");
    audio_file = "audio.wav"
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio).lower()
        print("You said: " + text)
    except sr.UnknownValueError:
        text = ""
        print("Google Web Speech API could not understand audio.")
    except sr.RequestError as e:
        text = ""
        print("Could not request results from Google Web Speech API; {0}".format(e))
    return text
while True:
    text = rec(3)
    print(text)
    if "remmacs" in text or "remix" in text or "remax" in text or "remarks" in text or "rema" in text:
        audio_gen("hey there")
        while True:
            text = rec(5)
            if "time" in text:
                text = time()
            elif "goodbye" in text:
                audio_gen("goodbye")
                break
            elif "play" in text:
                mus(text)
            else:
                text = text.replace(" ", "%20")
                text = send_message(text)
            print(text)
            audio_gen(text)
