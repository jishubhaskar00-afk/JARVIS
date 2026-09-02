import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import urllib.request
import urllib.parse
import json
import os
import sys
import time
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # reads variables from a local .env file (not committed to git)

# Try importing gTTS and pygame for natural voice playback
try:
    from gtts import gTTS
    import pygame
    pygame.mixer.init()
    USE_GTTS = True
except Exception:
    USE_GTTS = False

# ====================================================================
# CONFIGURATION & API KEYS
# ====================================================================
# Keys are read from environment variables / a local .env file.
# NEVER hardcode real keys here — that's what triggers GitHub push protection
# and leaks your credentials to anyone who reads the repo.
# Supports Groq keys (starting with gsk_) or OpenAI keys (starting with sk-)
AI_API_KEY = os.environ.get("AI_API_KEY", "")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "")

recognizer = sr.Recognizer()


def speak(text):
    """
    Speaks the text aloud through the speakers.
    Uses gTTS + pygame for high quality voice, or falls back to pyttsx3.
    """
    print(f"[Jarvis]: {text}")

    # 1. Try gTTS + pygame playback
    if USE_GTTS:
        try:
            filename = "temp_voice.mp3"
            tts = gTTS(text=text, lang="en", slow=False)
            tts.save(filename)

            # Load and play audio file
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.05)
            pygame.mixer.music.unload()

            if os.path.exists(filename):
                try:
                    os.remove(filename)
                except Exception:
                    pass
            return
        except Exception as e:
            print(f"[gTTS error, falling back to pyttsx3]: {e}")

    # 2. 100% Reliable Offline Fallback (pyttsx3)
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 175)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[pyttsx3 Error]: {e}")


def fetch_free_ai_summary(query):
    """Free instant Wikipedia answer engine (No API keys needed)."""
    clean = query.lower().strip()
    for prefix in ["who is", "who was", "what is", "what was", "tell me about", "define", "explain", "meaning of", "search for"]:
        if clean.startswith(prefix):
            clean = clean[len(prefix):].strip()
            break

    if not clean:
        return None

    try:
        encoded = urllib.parse.quote(clean)
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisVoiceAssistant/2.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                extract = data.get("extract")
                if extract:
                    sentences = extract.split(". ")
                    summary = ". ".join(sentences[:2])
                    if not summary.endswith("."):
                        summary += "."
                    return summary
    except Exception:
        pass
    return None


def aiProcess(command):
    """
    Processes queries with Groq / OpenAI or free instant fallback.
    """
    cmd = command.lower().strip()
    if cmd in ["hello", "hi", "hey"]:
        return "Hello! How can I help you today?"
    if "how are you" in cmd:
        return "I am doing great, thank you! How can I assist you?"
    if "who are you" in cmd or "what is your name" in cmd:
        return "I am Jarvis, your personal AI voice assistant."
    if "who made you" in cmd or "who created you" in cmd:
        return "I was built as a Python voice assistant by Jishu bhaskar."
    if "who is the owner of you" in cmd:
            return "My owner is jishu bhaskar, he is student of Diploma computer science and technology,his skils are HTML, CSS, Python , C programming language he is from murshidabad,jangipur,west bengal."

    # Check if API Key is configured
    if AI_API_KEY:
        try:
            # Auto-detect Groq vs OpenAI
            if AI_API_KEY.startswith("gsk_"):
                client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=AI_API_KEY)
                model = "allam-2-7b"
            else:
                client = OpenAI(api_key=AI_API_KEY)
                model = "gpt-4o-mini"

            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are Jarvis, a concise and helpful AI voice assistant. Provide direct answers in 1 to 2 short sentences suitable for text-to-speech."
                    },
                    {"role": "user", "content": command}
                ],
                max_tokens=100,
                timeout=10
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"[AI Service Error]: {e}")

    # Free Fallback Engine (Wikipedia REST API)
    free_summary = fetch_free_ai_summary(command)
    if free_summary:
        return free_summary

    return f"I couldn't find an answer for {command}."


def extract_song_title(c):
    """
    Detects if the user is asking to play a song/music,
    and returns the extracted song title.
    """
    c_lower = c.lower().strip()

    # 1. Direct match with preset library keys
    for key in musicLibrary.music:
        if key == c_lower or f" {key} " in f" {c_lower} ":
            return key

    # 2. Check keywords
    keywords = ["play", "song", "music", "track", "gana", "listen to", "audio"]
    if any(kw in c_lower for kw in keywords):
        cleaned = f" {c_lower} "
        for word in ["jarvis", "please", "can you", "could you", "listen to", "play", "song", "music", "track", "gana", "the", "a"]:
            cleaned = cleaned.replace(f" {word} ", " ")
        cleaned = " ".join(cleaned.split()).strip()
        if cleaned:
            return cleaned

    return None


def processCommand(c):
    """Processes user voice commands."""
    c = c.lower().strip()
    print(f"[Processing Command]: {c}")

    # 1. Exit Commands
    if any(stop_word in c for stop_word in ["exit", "quit", "shutdown", "bye", "goodbye"]):
        speak("Goodbye! Have a great day.")
        sys.exit(0)

    # 2. Time & Date Commands
    if "what time" in c or c == "time" or "current time" in c:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
        return
    if "what date" in c or "today's date" in c or c == "date":
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {current_date}")
        return

    # 3. Web Browsing Shortcuts
    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
        return
    if "open facebook" in c:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
        return
    if "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
        return
    if "open linkedin" in c:
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")
        return
    if "open github" in c:
        speak("Opening GitHub")
        webbrowser.open("https://www.github.com")
        return
    if "open instagram" in c:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")
        return

    # 4. Music Playback (Presets + YouTube fallback for ANY song)
    song = extract_song_title(c)
    if song:
        found = musicLibrary.play_song(song)
        if found:
            speak(f"Playing {song} from music library")
        else:
            speak(f"Searching and playing {song} on YouTube")
        return

    # 5. News Headlines
    if "news" in c or "headline" in c:
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
            req = urllib.request.Request(url, headers={"User-Agent": "JarvisAssistant/2.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    articles = data.get("articles", [])
                    if not articles:
                        speak("I couldn't find any news right now.")
                    else:
                        speak("Here are top news headlines:")
                        for i, article in enumerate(articles[:4], 1):
                            title = article.get("title", "")
                            if title:
                                speak(f"Headline {i}: {title}")
                else:
                    speak("Could not fetch news right now.")
        except Exception as e:
            print(f"[News Error]: {e}")
            speak("I couldn't fetch news due to a network issue.")
        return

    # 6. AI Question / Answer Process
    output = aiProcess(c)
    speak(output)


if __name__ == "__main__":
    speak("Initializing Jarvis...")
    print("\n" + "=" * 55)
    print("Calibrating microphone for ambient noise once...")
    
    # Calibrate ambient noise once at startup
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1.0)
    recognizer.dynamic_energy_threshold = False

    print("Jarvis is online and ready! Say 'Jarvis' to activate.")
    print("=" * 55 + "\n")

    while True:
        try:
            with sr.Microphone() as source:
                print("[Status]: Listening for wake word 'Jarvis'...")
                audio = recognizer.listen(source, timeout=4, phrase_time_limit=4)

            word = recognizer.recognize_google(audio)
            print(f"[Heard]: {word}")

            if "jarvis" in word.lower():
                speak("Yes, how can I help you?")
                with sr.Microphone() as source:
                    print("[Status]: Jarvis Active - Listening for your command...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)

                command = recognizer.recognize_google(audio)
                print(f"[Command]: {command}")
                processCommand(command)

        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"[Google Speech Recognition Error]: {e}")
        except KeyboardInterrupt:
            print("\n[Jarvis]: Shutting down. Goodbye!")
            speak("Shutting down. Goodbye!")
            break
        except Exception as e:
            print(f"[Error]: {e}")