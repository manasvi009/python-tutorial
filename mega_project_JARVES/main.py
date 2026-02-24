import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import subprocess
import platform
import urllib.parse

# Configuration - Update these with your actual API keys
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"  # Replace with your OpenAI API key
NEWS_API_KEY = "YOUR_NEWS_API_KEY_HERE"      # Replace with your NewsAPI key

recognizer = sr.Recognizer()
engine = pyttsx3.init() 

# Configure speech engine
engine.setProperty('rate', 150)    # Speed of speech
engine.setProperty('volume', 0.9)  # Volume level

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

# Initialize pygame mixer once globally
pygame.mixer.init()

def speak(text):
    """Convert text to speech using gTTS"""
    if not text or not text.strip():
        return
        
    temp_file = "temp_speech.mp3"
    try:
        # Create gTTS object and save to file
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(temp_file)
        
        # Load and play the audio
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        
        # Wait for playback to complete
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        # Clean up
        pygame.mixer.music.unload()
        
    except Exception as e:
        print(f"Speech error: {e}")
        # Fallback to pyttsx3
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e2:
            print(f"Fallback speech also failed: {e2}")
    finally:
        # Remove temporary file
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except:
            pass 

def launch_app(app_name):
    """Launch applications on Windows"""
    app_commands = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "chrome": "chrome.exe",
        "firefox": "firefox.exe",
        "edge": "msedge.exe",
        "vlc": "vlc.exe",
        "spotify": "spotify.exe",
        "steam": "steam.exe",
        "discord": "discord.exe",
        "vs code": "code.exe",
        "code": "code.exe",
        "sublime": "sublime_text.exe",
        "photoshop": "photoshop.exe",
        "illustrator": "illustrator.exe",
        "cmd": "cmd.exe",
        "command prompt": "cmd.exe",
        "powershell": "powershell.exe",
        "explorer": "explorer.exe",
        "file manager": "explorer.exe",
        "control panel": "control.exe",
        "settings": "start ms-settings:",
        "task manager": "taskmgr.exe"
    }
    
    app_name = app_name.lower().strip()
    
    if app_name in app_commands:
        try:
            command = app_commands[app_name]
            if command.startswith("start "):
                # For special commands like settings
                os.system(command)
            else:
                # For regular applications
                subprocess.Popen(command)
            return True
        except Exception as e:
            print(f"Error launching {app_name}: {e}")
            return False
    else:
        # Try to find the app in common locations
        try:
            username = os.getlogin()
        except:
            # Fallback if os.getlogin() fails
            username = os.environ.get('USERNAME', 'default')
        
        common_paths = [
            f"C:\\Program Files\\{app_name}\\{app_name}.exe",
            f"C:\\Program Files (x86)\\{app_name}\\{app_name}.exe",
            f"C:\\Users\\{username}\\AppData\\Local\\{app_name}\\{app_name}.exe"
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                try:
                    subprocess.Popen(path)
                    return True
                except Exception as e:
                    print(f"Error launching from {path}: {e}")
                    continue
        return False

def search_youtube_video(query):
    """Search for a video on YouTube and open it"""
    try:
        # Format the search query
        search_query = query.replace("play", "").replace("youtube", "").replace("on youtube", "").strip()
        if not search_query:
            return False
            
        # Create YouTube search URL
        search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}"
        
        # Open the search results
        webbrowser.open(search_url)
        return True
    except Exception as e:
        print(f"Error searching YouTube: {e}")
        return False

def aiProcess(command):
    """Process command using OpenAI"""
    if OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
        return "Please configure your OpenAI API key in the code to use AI features."
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis. Give short, clear responses. Be helpful and friendly."},
                {"role": "user", "content": command}
            ],
            max_tokens=100
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        print(f"AI processing error: {e}")
        return "Sorry, I'm having trouble processing that request right now."

def processCommand(c):
    command = c.lower()
    
    # YouTube video playing commands (prioritized first)
    if "play" in command and "youtube" in command:
        speak("Searching YouTube for your video")
        if search_youtube_video(command):
            speak("I've opened YouTube with your search results")
        else:
            speak("Sorry, I couldn't search YouTube right now")
        return True  # Continue running in main loop
    
    elif command.startswith("youtube") and "play" in command:
        speak("Searching YouTube for your video")
        if search_youtube_video(command):
            speak("I've opened YouTube with your search results")
        else:
            speak("Sorry, I couldn't search YouTube right now")
        return True  # Continue running in main loop
        
    elif "search youtube for" in command:
        speak("Searching YouTube for your query")
        if search_youtube_video(command):
            speak("I've opened YouTube with your search results")
        else:
            speak("Sorry, I couldn't search YouTube right now")
        return True  # Continue running in main loop
    
    # Web browsing commands (prioritized over app launching to avoid confusion)
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
        return True  # Continue running in main loop
        
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
        return True  # Continue running in main loop
        
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
        return True  # Continue running in main loop
        
    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
        return True  # Continue running in main loop
    
    # App launching commands (lower priority to avoid conflicts with web commands)
    elif command.startswith("open") or command.startswith("launch"):
        app_name = command.replace("open", "").replace("launch", "").strip()
        if app_name:
            # Check if it's a known website name to avoid confusion
            if app_name in ["google", "youtube", "facebook", "linkedin"]:
                speak(f"Opening {app_name}")
                if app_name == "google":
                    webbrowser.open("https://google.com")
                elif app_name == "youtube":
                    webbrowser.open("https://youtube.com")
                elif app_name == "facebook":
                    webbrowser.open("https://facebook.com")
                elif app_name == "linkedin":
                    webbrowser.open("https://linkedin.com")
            else:
                speak(f"Opening {app_name}")
                if launch_app(app_name):
                    speak(f"{app_name} has been opened successfully")
                else:
                    speak(f"Sorry, I couldn't find or open {app_name}")
        else:
            speak("Please specify which application to open")
        return True  # Continue running in main loop
    
    elif "start" in command and ("app" in command or "application" in command):
        # Handle "start [app name] app" format
        words = command.split()
        if "start" in words:
            start_index = words.index("start")
            if start_index + 1 < len(words):
                app_name = words[start_index + 1]
                speak(f"Starting {app_name}")
                if launch_app(app_name):
                    speak(f"{app_name} has been started")
                else:
                    speak(f"Sorry, I couldn't start {app_name}")
        return True  # Continue running in main loop
    
    elif command.startswith("play"):
        try:
            song = command.split(" ")[1]
            link = musicLibrary.music[song]
            webbrowser.open(link)
        except:
            speak("Please specify which song to play")
        return True  # Continue running in main loop

    elif "news" in command:
        if NEWS_API_KEY == "YOUR_NEWS_API_KEY_HERE":
            speak("Please configure your NewsAPI key to get news updates.")
            return True  # Continue running in main loop
            
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}")
            if r.status_code == 200:
                # Parse the JSON response
                data = r.json()
                
                # Extract the articles
                articles = data.get('articles', [])
                
                if articles:
                    speak("Here are the latest headlines:")
                    # Speak first 3 headlines
                    for i, article in enumerate(articles[:3]):
                        speak(f"Headline {i+1}: {article['title']}")
                else:
                    speak("No news articles found at the moment.")
            else:
                speak("Sorry, I couldn't fetch the news right now.")
        except Exception as e:
            print(f"News error: {e}")
            speak("Sorry, I'm having trouble fetching news right now.")
        return True  # Continue running in main loop

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output)
        return True  # Continue running in main loop

if __name__ == "__main__":
    # Initialize recognizer with better settings
    r = sr.Recognizer()
    r.energy_threshold = 400
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.8
    r.phrase_threshold = 0.3
    r.non_speaking_duration = 0.5
    
    # Configure microphone settings
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait 2 seconds.")
            print("🎵 Make sure to speak clearly and at normal volume")
            r.adjust_for_ambient_noise(source, duration=2)
            print(f"Energy threshold set to: {r.energy_threshold}")
            print("Microphone calibrated!")
    except Exception as e:
        print(f"Microphone setup error: {e}")
        print("Make sure you have a working microphone connected.")
    
    speak("Initializing Jarvis....")
    print("🎙️  Jarvis is ready! Say 'Jarvis' to activate me.")
    print("💡 Tip: Speak clearly and pause slightly between words")
    
    while True:
        try:
            # Listen for the wake word "Jarvis"
            with sr.Microphone() as source:
                print("\n👂 Listening for 'Jarvis' (wake word)...")
                # Better audio listening settings
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
            
            # Try to recognize the wake word
            try:
                word = r.recognize_google(audio, show_all=False)
                print(f"🔍 Heard: '{word}'")
                
                if word.lower() == "jarvis":
                    speak("Yes, how can I help you?")
                    print("✅ Jarvis activated! Listening for command...")
                    
                    # Listen for command with better settings
                    with sr.Microphone() as source:
                        print("👂 Listening for your command...")
                        audio = r.listen(source, timeout=8, phrase_time_limit=6)
                    
                    try:
                        command = r.recognize_google(audio, show_all=False)
                        print(f"📝 Command received: '{command}'")
                        processCommand(command)
                    except sr.UnknownValueError:
                        speak("Sorry, I didn't catch that. Please try again.")
                        print("❌ Could not understand the command")
                    except sr.RequestError as e:
                        speak("Sorry, speech service is unavailable right now.")
                        print(f"❌ Speech service error: {e}")
                        
                else:
                    print(f"⏭️  Not the wake word. Heard: '{word}'")
                    
            except sr.UnknownValueError:
                print("🔇 No clear speech detected")
                continue
            except sr.RequestError as e:
                print(f"❌ Speech recognition service error: {e}")
                speak("Sorry, I'm having trouble with speech recognition.")
                
        except sr.WaitTimeoutError:
            # This is normal - just continue listening
            print("⏰ Still listening...")
            continue
        except sr.UnknownValueError:
            print("Could not understand audio, trying again...")
            continue
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
            speak("Sorry, I'm having trouble with speech recognition.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            speak("Sorry, something went wrong. Please try again.")