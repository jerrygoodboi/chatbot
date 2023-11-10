source /home/ncerc/venv/bin/activate 
#!/bin/python3
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
elevenlabs.set_api_key("fbaab3584cf611c03ebc321df93e0824")
#
conversation = "This is a conversation between User and remmacs, a  friendly chatbot. remmacs is helpful, kind, honest, good at writing, and never fails to answer any requests immediately and with precision and remmacs replies within one sentence. " 
def send_post_request(url, data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response content:")
        print(response.text)
        return None
def comp(text):
    # Initialize conversation history with an initial prompt
    global conversation
    while True:
        user_input = text 
        conversation += "User: " + user_input + "\n" + "remmacs:"

        # Create a JSON request with the entire conversation
        json_request = {
                "n_predict": 50,
                "temperature": 0.7,
                "stop": ["</s>", "remmacs:", "User:"],
                "repeat_last_n": 256,
                "repeat_penalty": 1.2,
                "top_k": 40,
                "top_p": 0.5,
                "tfs_z": 1,
                "typical_p": 1,
                "presence_penalty": 0,
                "frequency_penalty": 0,
                "mirostat": 0,
                "mirostat_tau": 5,
                "mirostat_eta": 0.1,
                "grammar": "",
                "n_probs": 0,
                "image_data": [],
                "cache_prompt": True,
                "slot_id": 0,
                "prompt": conversation
                }
        # Send the request and get the response
        response = send_post_request("http://127.0.0.1:8080/completion", json_request)

        if response:
            if "content" in response:
                chatbot_response = response["content"]
                conversation += chatbot_response + "\n" 
                return chatbot_response
            else:
                print("Chatbot: No response from the server.")
        else:
            print("Request failed. Check the server or URL.") 
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
def audio_gen(text):
    audio = elevenlabs.generate(
            text,
            voice = "Glinda"
            )
    elevenlabs.save(audio, "output.mp3")
    os.system("mplayer output.mp3 &> /dev/null")
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
                print(text)
                audio_gen(text)
            elif "goodbye" in text:
                audio_gen("goodbye")
                break
            elif "play" in text:
                mus(text)
            elif text:
                text = comp(text)
                text.replace("remmacs:","",1)
                print(text)
                audio_gen(text)
