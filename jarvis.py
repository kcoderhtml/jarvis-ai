# import speech and audio libraries
import speech_recognition as sr
import struct
import pyaudio
import subprocess
import pvporcupine
# import openai library
import openai
# import env libraries
import json
import os
from dotenv import load_dotenv

# load .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
porcupine_api_key = os.getenv("PORCUPINE_API_KEY")

# set up command lookup array
command_lookup = {
    "conversation": ["echo", ""],
    "play discover weekly": ["osascript", "-e", 'tell application "Spotify" to play track "spotify:playlist:37i9dQZEVXcMaWCjUILjal"'],
    "exit": ["exit"],
}
commands_string = str(list(command_lookup.keys()))  # Convert array to string

# set up speech recognition
r = sr.Recognizer()
m = sr.Microphone()

porcupine = None
sound = None
audio_stream = None

def say(text):
    print(text)
    subprocess.call(["say", text])

def execute_command(command):
    subprocess.call(command)

def handle_response(response):
    try:
        assistant = json.loads(response)
    except json.decoder.JSONDecodeError:
        say("Error decoding JSON response")
        return
    
    if assistant['response'] is not None:
        say(assistant['response'])
    elif assistant['command'] is not None:
        if assistant['command'] == ["exit"]:
            print("Exiting...")
            exit()
        else:
            execute_command(assistant['command'])
    else:
        print("Command not recognized.")
        return

def get_gpt(command):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Jarvis, a dry, snarky, ai assistant. Based on the below input, select the best command to execute from the following array. Return only the command that should be executed from the array and a response as a JSON object. " + commands_string},
            {"role": "user", "content": "Input:" + command}
        ]
    )

    if response["choices"][0]["message"]["role"] == "assistant":
        gpt_response = response["choices"][0]["message"]["content"]
        print("GPT-3:", gpt_response)
        handle_response(gpt_response)
    else:
        say("Sorry, something went wrong with my brain.")

# Start listening for commands
try:
    say("Initializing...")
    porcupine = pvporcupine.create(
        access_key=porcupine_api_key,
        keyword_paths=["Hey-Jarvis_en_mac_v2_2_0/Hey-Jarvis_en_mac_v2_2_0.ppn"]
        )

    sound = pyaudio.PyAudio()
    
    audio_stream = sound.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)
    
    with m as source: r.adjust_for_ambient_noise(source)
    
    listening = False
    
    say("Initialized")
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)
        
        if keyword_index >= 0:
            listening = True
            print("Hotword Detected")
            
        if listening:
            with m as source: audio = r.listen(source)
            try:
                value = r.recognize_google(audio)
                print("You said {}".format(value))
            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
            finally:
                listening = False
            
except KeyboardInterrupt:
    print("Stopping....")

finally:
    if porcupine is not None:
        porcupine.delete()

    if audio_stream is not None:
        audio_stream.close()

    if sound is not None:
        sound.terminate()