import speech_recognition as sr
import subprocess
import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
wake_word = os.getenv("WAKE_WORD")

command_lookup = {
    "conversation": ["echo", ""],
    "play discover weekly": ["osascript", "-e", 'tell application "Spotify" to play track "spotify:playlist:37i9dQZEVXcMaWCjUILjal"'],
    "exit": ["exit"],
}

commands_string = str(list(command_lookup.keys()))  # Convert array to string

def say(text):
    subprocess.call(["say", text])

def execute_command(command):
    subprocess.call(command)

def transcribe_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        # change text to lowercase for matching purposes
        text = text.lower()

        print("Heard:", text)
        if wake_word in text:
            get_gpt(text)
        else:
            print("Command not recognized.")
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Error: {e}")

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
        try:
            assistant = json.loads(gpt_response)
        except json.decoder.JSONDecodeError:
            print("Error decoding JSON response")
            return
        say(assistant['response'])
    else:
        print("Jarvis: Sorry, I didn't understand that command.")
        say("Sorry, I didn't understand that command.")

    # Perform the corresponding action based on the assistant's response
    command = command_lookup.get(assistant['command'])
    if command is not None:
        if command == ["exit"]:
            print("Exiting...")
            exit()
        else:
            execute_command(command)
    else:
        print("Command not recognized.")
        return

# Start listening for commands
try:
    while True:
        transcribe_audio()
except KeyboardInterrupt:
    print("Stopping...")