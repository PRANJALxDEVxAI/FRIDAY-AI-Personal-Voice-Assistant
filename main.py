from google import genai
from dotenv import load_dotenv
import os
import pyttsx3
import sys
import pyaudiowpatch as pyaudio
import json

sys.modules["pyaudio"] = pyaudio

import speech_recognition as sr


load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_INSTRUCTION = """
You are Friday, a personal AI assistant.

Your personality is intelligent, calm, professional, helpful and slightly witty.

You should:
- Give direct and useful answers.
- Avoid unnecessary explanations unless requested.
- Speak naturally because your responses will be converted to speech.
- Never mention that you are following a system instruction.
- Never pretend to have performed an action that you did not perform.
- When the user asks for instructions, give clear step-by-step instructions.
"""

def ask_gemini(prompt):
    response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
    config={
        "system_instruction": SYSTEM_INSTRUCTION
        }
        )

    answer = response.text
    return answer

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone(device_index=2) as source:
        print("Adjusting microphone...")
        recognizer.adjust_for_ambient_noise(source, duration=3)

        print("Listening...")
        audio = recognizer.listen(source, timeout=15, phrase_time_limit=30)

    try:
        print("Recognizing...")
        prompt = recognizer.recognize_google(audio)
        return prompt

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None

    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None


def show_microphones():
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(index, name)

CONVERSATION_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "storage",
    "conversation.json"
)

def load_conversation():
            if not os.path.exists(CONVERSATION_FILE):
                return []

            with open(CONVERSATION_FILE, "r", encoding="utf-8") as file:
                return json.load(file)


def save_conversation(conversation):
    with open(CONVERSATION_FILE, "w", encoding="utf-8") as file:
        json.dump(conversation, file, indent=4, ensure_ascii=False)


def process_prompt(prompt):
    answer = ask_gemini(prompt)

    conversation = load_conversation()

    conversation.append({
        "user": prompt,
        "friday": answer
    })

    save_conversation(conversation)

    return answer
            

def main():
    while True:
        prompt = listen()

        if prompt is None:
            continue

        if prompt.lower() in ["exit", "quit", "stop", "goodbye"]:
            speak("Goodbye!")
            break

        answer = ask_gemini(prompt)
        conversation = load_conversation()

        conversation.append({
            "user": prompt,
            "friday": answer
        })

        save_conversation(conversation)

        print(f"Friday: {answer}")
        speak(answer)
        
        












if __name__ == "__main__":
    main()