import speech_recognition as sr
import subprocess
import openai
import json
import os
from dotenv import load_dotenv


load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

wake_word = "hey jarvis"

commands = ["open terminal", "close terminal"]

delimiter = ', '  # Delimiter between array elements
commands_string = '[' + delimiter.join(map(str, commands)) + ']'  # Convert array to string

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
        if "hey jarvis" in text:
            execute_command(text)
        else:
            print("Command not recognized.")
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Error: {e}")

def execute_command(command):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Jarvis, a snarky, artificial assistant created by Kieran Klukas. You will occasionally make fun of the request in a round about way, but always obey. Based on the below input, select the best command to execute from the following array. If there isn't a good command to execute, then say 'none'. Return only the command that should be executed from the array and a response as a JSON object" + commands_string},
            {"role": "user", "content": "Input:" + command}
        ]
    )

    if response["choices"][0]["message"]["role"] == "assistant":
        gpt_response = response["choices"][0]["message"]["content"]
        print("GPT-3:", gpt_response)
        assistant = json.loads(gpt_response)
        print("Jarvis:", assistant['response'])
    else:
        print("Jarvis: Sorry, I didn't understand that command.")

    # Perform the corresponding action based on the assistant's response
    if "open terminal" in assistant['command']:
        subprocess.run(["open", "-a", "Terminal"])
    elif "close terminal" in assistant['command']:
        subprocess.run(["osascript", "-e", 'quit app "Terminal"'])
    # Add more command-action mappings as needed
    else:
        print("Command not recognized.")

# Start listening for commands
try:
    while True:
        transcribe_audio()
except KeyboardInterrupt:
    print("Stopping...")