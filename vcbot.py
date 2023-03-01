import os
from dotenv.main import load_dotenv
import openai
import speech_recognition as sr
import pyttsx3

load_dotenv()
openai.api_key = os.getenv('SUPERSECRETAPIKEY')

engine = pyttsx3.init()
voices = engine.getProperty("voices")

r = sr.Recognizer()
mic = sr.Microphone(device_index=4)

user_name = "User"
bot_name = "VcBot"
conversation = ""

while True:
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source, timeout=5, phrase_time_limit=10)

    try:
        user_input = r.recognize_google(audio)
    except:
        continue

    prompt = user_name + ": " + user_input + "\n" + bot_name + ": "
    conversation += prompt

    response = openai.Completion.create(
        engine='text-davinci-003', prompt=conversation, max_tokens=2000)
    response_str = response["choices"][0]["text"].replace("\n", "")
    response_str = response_str.split(
        user_name + ": ", 1)[0].split(bot_name + ": ", 1)[0]
    conversation += response_str + "\n"

    # Print the prompt from the user and the response from the chatbot in the terminal
    print(user_name + ": " + user_input)
    print(bot_name + ": " + response_str)

    engine.setProperty("voice", voices[1].id)
    engine.say(response_str)
    engine.runAndWait()
