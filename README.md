# 🤖 Jarvis – AI Voice Assistant

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)

Jarvis is a **Python-based AI voice assistant** designed to interact with users through voice commands. It can recognize speech, respond using natural voice, answer questions with AI, open popular websites, fetch news headlines, and play music through YouTube.

## ✨ Features

* 🎙️ **Voice Recognition** – Activate Jarvis using the wake word `"Jarvis"`
* 🧠 **AI-Powered Q&A** – Ask questions and receive concise AI-generated answers
* 🔊 **Text-to-Speech** – Responds with natural voice using gTTS/pygame with pyttsx3 fallback
* 🌐 **Web Shortcuts** – Open Google, YouTube, Facebook, LinkedIn, GitHub, and Instagram
* 📰 **News Headlines** – Fetches the latest top headlines using NewsAPI
* 🎵 **Music Player** – Plays songs from a preset music library or searches YouTube
* 📅 **Date & Time** – Provides the current date and time
* 🔄 **Fallback System** – Uses Wikipedia for basic information when the AI service is unavailable
* ⚡ **Command-Based Automation** – Performs different actions based on natural voice commands

## 🛠️ Technologies Used

* Python
* SpeechRecognition
* OpenAI API
* Groq API
* gTTS
* pygame
* pyttsx3
* NewsAPI
* Wikipedia REST API
* YouTube
* Webbrowser

## 📂 Project Structure

```text
Jarvis/
│
├── main.py
├── client.py
├── musicLibrary.py
└── README.md
```

## 🚀 How It Works

1. Start Jarvis.
2. Jarvis calibrates the microphone.
3. Say **"Jarvis"** to activate the assistant.
4. Speak your command.
5. Jarvis recognizes the command and performs the requested action.
6. Jarvis responds using voice.

## 🎯 Example Commands

```text
"Jarvis, what is coding?"
"Jarvis, what time is it?"
"Jarvis, open YouTube"
"Jarvis, open GitHub"
"Jarvis, give me the news"
"Jarvis, play Believer"
"Jarvis, who are you?"
```

## 👨‍💻 Author

**Jishu Bhaskar**

A Computer Science & Technology student passionate about **Python, Software Development, Web Development, and AI/ML**.

⭐ If you like this project, consider giving the repository a star!
