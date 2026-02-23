import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import pygame
import os
import time
import subprocess
import platform
import urllib.parse
from gtts import gTTS

# Configuration
recognizer = sr.Recognizer()
engine = pyttsx3.init() 

# Configure speech engine
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

# Initialize pygame mixer
pygame.mixer.init()

def speak(text):
    """Convert text to speech using gTTS with pyttsx3 fallback"""
    if not text or not text.strip():
        return
        
    print(f"🔊 Speaking: {text}")
    
    # Try gTTS first (actual speech output)
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
        print(f"gTTS error: {e}")
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
        common_paths = [
            f"C:\\Program Files\\{app_name}\\{app_name}.exe",
            f"C:\\Program Files (x86)\\{app_name}\\{app_name}.exe",
            f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\{app_name}\\{app_name}.exe"
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

def processCommand(c):
    """Process voice commands without API keys"""
    command = c.lower()
    
    # YouTube video playing commands
    if "play" in command and "youtube" in command:
        speak("Searching YouTube for your video")
        if search_youtube_video(command):
            speak("I've opened YouTube with your search results")
        else:
            speak("Sorry, I couldn't search YouTube right now")
        return True
        
    elif command.startswith("youtube") and "play" in command:
        speak("Searching YouTube for your video")
        if search_youtube_video(command):
            speak("I've opened YouTube with your search results")
        else:
            speak("Sorry, I couldn't search YouTube right now")
        return True
        
    elif "search youtube for" in command:
        speak("Searching YouTube for your query")
        if search_youtube_video(command):
            speak("I've opened YouTube with your search results")
        else:
            speak("Sorry, I couldn't search YouTube right now")
        return True
    
    # App launching commands
    if command.startswith("open") or command.startswith("launch"):
        app_name = command.replace("open", "").replace("launch", "").strip()
        if app_name:
            speak(f"Opening {app_name}")
            if launch_app(app_name):
                speak(f"{app_name} has been opened successfully")
            else:
                speak(f"Sorry, I couldn't find or open {app_name}")
        else:
            speak("Please specify which application to open")
        return True  # Continue running
    
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
        return True  # Continue running
    
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
        return True  # Continue running
        
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
        return True  # Continue running
        
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
        return True  # Continue running
        
    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
        return True  # Continue running
        
    elif command.startswith("play"):
        try:
            song = command.split(" ")[1]
            if song in musicLibrary.music:
                speak(f"Playing {song}")
                webbrowser.open(musicLibrary.music[song])
            else:
                speak("Sorry, I don't have that song in my library")
        except:
            speak("Please specify which song to play")
        return True  # Continue running
            
    elif "hello" in command or "hi" in command:
        speak("Hello! How can I help you today?")
        return True  # Continue running
        
    elif "how are you" in command:
        speak("I'm doing great, thank you for asking!")
        return True  # Continue running
        
    elif "what time" in command:
        import datetime
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
        return True  # Continue running
        
    elif "what day" in command or "what date" in command:
        import datetime
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {today}")
        return True  # Continue running
        
    elif "thank you" in command or "thanks" in command:
        speak("You're welcome!")
        return True  # Continue running
        
    elif "bye" in command or "goodbye" in command:
        speak("Goodbye! Have a great day!")
        return False  # Signal to exit
        
    else:
        speak("I can help you with: opening websites, launching applications, playing music, searching YouTube, telling time, or having a simple conversation. Try saying 'play music on YouTube' or 'search YouTube for tutorials'. What would you like me to do?")
        return True  # Continue running

def main():
    """Main function to run the assistant"""
    print("=== Jarvis Virtual Assistant ===")
    print("Features available without API keys:")
    print("- Web browsing (Google, Facebook, YouTube, LinkedIn)")
    print("- Application launching (Notepad, Calculator, Chrome, etc.)")
    print("- Music playback")
    print("- YouTube video search and play")
    print("- Basic conversation")
    print("- Time and date")
    print("===============================")
    
    # Initialize recognizer with better settings
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 400  # Adjust for your environment
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8   # Pause between words
    recognizer.phrase_threshold = 0.3  # Minimum phrase time
    recognizer.non_speaking_duration = 0.5  # Time before speech ends
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait 2 seconds.")
            print("🎵 Make sure to speak clearly and at normal volume")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print(f"Energy threshold set to: {recognizer.energy_threshold}")
            print("Microphone ready!")
    except Exception as e:
        print(f"Microphone setup error: {e}")
        print("Running in text mode instead...")
        text_mode()
        return
    
    speak("Hello! I'm Jarvis. Say my name to activate me.")
    print("🎙️  Say 'Jarvis' to activate, or say 'bye' to exit.")
    print("💡 Tip: Speak clearly and pause slightly between words")
    
    running = True
    while running:
        try:
            with sr.Microphone() as source:
                print("\n👂 Listening for 'Jarvis' (wake word)...")
                # Better audio listening settings
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            
            # Try to recognize the wake word
            try:
                word = recognizer.recognize_google(audio, show_all=False)
                print(f"🔍 Heard: '{word}'")
                
                if word.lower() == "jarvis":
                    speak("Yes, how can I help you?")
                    print("✅ Jarvis activated! Listening for your command...")
                    
                    # Listen for actual command with better settings
                    with sr.Microphone() as source:
                        print("👂 Listening for your command...")
                        audio = recognizer.listen(source, timeout=8, phrase_time_limit=6)
                    
                    try:
                        command = recognizer.recognize_google(audio, show_all=False)
                        print(f"📝 Command received: '{command}'")
                        
                        # Process the command and get whether to continue
                        should_continue = processCommand(command)
                        if not should_continue:
                            running = False
                            
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
            continue
        except sr.UnknownValueError:
            continue
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            speak("Sorry, I'm having trouble with speech recognition.")
        except Exception as e:
            print(f"Error: {e}")
            speak("Sorry, something went wrong.")

def text_mode():
    """Text-based mode for testing without microphone"""
    print("\n=== Text Mode ===")
    print("Type your commands (type 'quit' to exit):")
    
    while True:
        command = input("\nYou: ").strip()
        if command.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break
            
        if command:
            result = processCommand(command)
            if not result:
                break

if __name__ == "__main__":
    main()