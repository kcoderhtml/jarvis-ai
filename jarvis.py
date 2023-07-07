import speech_recognition as sr
import subprocess
import openai
import json
import pvporcupine
import os
from dotenv import load_dotenv

load_dotenv()

porcupine_api_key = os.getenv("PORCUPINE_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

porcupine = pvporcupine.create(
  access_key=porcupine_api_key,
  keyword_paths="~/Hey-Jarvis_en_mac_v2_2_0/Hey-Jarvis_en_mac_v2_2_0.ppn"
)

wake_word = "hey jarvis"


commands = ["open terminal", "close terminal"]

delimiter = ', '  # Delimiter between array elements
commands_string = '[' + delimiter.join(map(str, commands)) + ']'

def get_next_audio_frame():
  pass

def listen_for_command():
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        while True:
            audio = r.listen(source)
            pcm = audio.frame_data

            # Detect wake word
            if porcupine.process(pcm):
                print("Wake word detected!")
                transcribed_text = transcribe_audio(r, audio)
                process_command(audio)
                break

def transcribe_audio(recognizer, audio):
    try:
        transcribed_text = recognizer.recognize_google(audio)
        return transcribed_text
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Error: {e}")
    return ""

def process_command(command):
    try:
        command = command.lower()

        print("Heard:", command)
        if wake_word in command:
            command = command.replace(wake_word, "").strip()
            execute_command(command)
        else:
            print("Wake word not detected.")
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
while True:
    listen_for_command()
