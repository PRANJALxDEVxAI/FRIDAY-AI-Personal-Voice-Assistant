# FRIDAY AI 🤖

A Python-based personal AI voice assistant inspired by **FRIDAY/JARVIS**.

FRIDAY combines voice input, AI-powered responses, text-to-speech, persistent conversation storage, and a real-time sci-fi desktop interface into a single assistant.

The project is being developed as a foundation for a more advanced personal AI system with future capabilities such as automation, memory, AI/ML integration, RAG, and system control.

---

## ✨ Features

- 🎙️ **Voice Input**
  - Captures speech through the system microphone.
  - Converts speech into text using SpeechRecognition.

- 🧠 **AI Responses**
  - Uses Google's Gemini API to generate intelligent responses.
  - Designed with a custom personality and system instruction for FRIDAY.

- 🔊 **Text-to-Speech**
  - Converts FRIDAY's responses into spoken audio using `pyttsx3`.

- 💾 **Conversation Memory**
  - Stores conversations locally in JSON format.
  - User prompts and FRIDAY responses are saved for persistent history.

- 🖥️ **Sci-Fi Desktop Interface**
  - Custom Tkinter interface.
  - Animated futuristic core/orb.
  - Real-time status indicators.
  - Animated visual elements and response display.

- ⚡ **Multithreaded Voice Processing**
  - Voice processing runs in a background thread.
  - Keeps the graphical interface responsive while FRIDAY listens, thinks, and speaks.

- 🔐 **Environment Variables**
  - API credentials are stored in `.env`.
  - Sensitive keys are not hardcoded into the source code.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Google Gemini API | AI response generation |
| Tkinter | Desktop graphical interface |
| SpeechRecognition | Speech-to-text |
| PyAudioWPatch | Microphone/audio input |
| pyttsx3 | Text-to-speech |
| python-dotenv | Environment variable management |
| JSON | Local conversation storage |
| Threading | Background voice processing |

---

## 📁 Project Structure

```text
FRIDAY_AI/
│
├── main.py
├── frontend.py
├── .env
│
└── storage/
    ├── instructions.json
    └── conversation.json
