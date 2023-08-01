# jarvis-ai

To run yourself you need to create an env file structured as follows:
```env
PICO_API_KEY="xxxxxxxxxxxxxxxxxxxxx=="
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxx"
WAKE_WORD="hey jarvis"
```
You can get a pico api key at [https://console.picovoice.ai/](https://console.picovoice.ai/).
![image](https://github.com/kcoderhtml/jarvis-ai/assets/92754843/cccd73f4-da04-4226-b88e-7f5c38a361b1)

You can create a new openapi key at [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys).
The api ends up being quite cheap. I used it to generate commit messages through gitlens, several side projects, and heavy testing on this project and only spent 8 cents.
![image](https://github.com/kcoderhtml/jarvis-ai/assets/92754843/a66bc4b0-cd7b-400f-a5b6-bb9ec578bace)
![image](https://github.com/kcoderhtml/jarvis-ai/assets/92754843/3b111b65-1df4-48f4-a1da-3e1a6d105b67)

If you want to customize the wake word then you need to replace the wake word in the env file as well as the wake word training data in /Hey-Jarvis_en_mac_v2_2_0/Hey-Jarvis_en_mac_v2_2_0.ppn with your own wake word. Go to [https://console.picovoice.ai/ppn](https://console.picovoice.ai/ppn) to train your own wake word file.

![image](https://github.com/kcoderhtml/jarvis-ai/assets/92754843/89715c75-4a51-4e42-acfa-36bb1ad187ae)
