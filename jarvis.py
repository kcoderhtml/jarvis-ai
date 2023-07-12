# import speech and audio libraries
import speech_recognition as sr
import subprocess
import pyttsx3
# import openai library
import openai
# import env libraries
import json
import os
from dotenv import load_dotenv

# load .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
wake_word = os.getenv("WAKE_WORD")

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

# set up text to speech
engine = pyttsx3.init()
engine.setProperty('rate', 190)

def say(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def execute_command(command):
    subprocess.call(command)

def handle_response(response):
    try:
        assistant = json.loads(response)
    except json.decoder.JSONDecodeError:
        say("Error decoding JSON response")
        return
    
    if assistant['message'] is not None:
        say(assistant['message'])
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
            {"role": "system", "content": "You are Jarvis, a dry, snarky, ai assistant. Based on the below input, select the best command to execute from the following array. Return only the command that should be executed from the array and a message as a JSON object. For conversation give a reply via the message key. Only give the json object. Commands:" + commands_string},
            {"role": "user", "content": "Input:" + command}
        ]
    )

    if response["choices"][0]["message"]["role"] == "assistant":
        gpt_response = response["choices"][0]["message"]["content"]
        print("GPT-3:", gpt_response)
        handle_response(gpt_response)
    else:
        say("Sorry, something went wrong with my brain.")

say("Initializing...")
# Start listening for commands
try:
    with m as source:
        r.adjust_for_ambient_noise(source)
    say("Initialized.")
    print("Say '" + wake_word + "' to wake me up.")
    while True:
            with m as source:
                audio = r.listen(source, phrase_time_limit=2)
            try:
                value = r.recognize_google(audio)
                if wake_word in value.lower():
                    say("Yes?")
                    with m as source:
                        audio = r.listen(source, phrase_time_limit=7)
                    try:
                        value = r.recognize_google(audio)
                        print(value)
                        say("thinking...")
                        get_gpt(value)
                    except sr.UnknownValueError:
                        print("Oops! Didn't catch that command")
                    except sr.RequestError as e:
                        print("Uh oh! Couldn't request results from Google Speech Recognition")
            except sr.UnknownValueError:
                print("Oops! Didn't catch that wake word")
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    print("Stopping....")
    engine.stop()
    exit()
except Exception as e:
    print("Error: ", e)