import pvporcupine
import os
from dotenv import load_dotenv
import pyaudio
import numpy as np
import pyautogui

load_dotenv()

porcupine_api_key = os.getenv("PORCUPINE_API_KEY")

porcupine = pvporcupine.create(
    access_key=porcupine_api_key,
    keyword_paths=["Hey-Jarvis_en_mac_v2_2_0/Hey-Jarvis_en_mac_v2_2_0.ppn"],
)

pa = pyaudio.PyAudio()

audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

def listen_for_wake_word():
    pcm = audio_stream.read(porcupine.frame_length,exception_on_overflow = False)
    pcm = np.frombuffer(pcm, dtype=np.int16)

    keyword_index = porcupine.process(pcm)

    if keyword_index >= 0:
        print('Wake word detected!')
        siri_trigger()
        
def siri_trigger():
    pyautogui.hotkey('command', 'space', interval=0.3)

# Start listening for the wake word
try:
    print("Listening for wake word...")
    while True:
        listen_for_wake_word()
except KeyboardInterrupt:
    print("Stopping...")
    audio_stream.close()
    pa.terminate()
    porcupine.delete()