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
import threading
import time
import queue
import sys
from datetime import datetime

# Configuration - Update these with your actual API keys
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"  # Replace with your OpenAI API key
NEWS_API_KEY = "YOUR_NEWS_API_KEY_HERE"      # Replace with your NewsAPI key

# Performance optimization settings
USE_OFFLINE_TTS = False  # Set to True for faster pyttsx3 only (no internet required)
ENABLE_COMMAND_CACHE = True  # Cache frequent responses
MAX_RETRIES = 3  # Maximum retry attempts for failed operations

# Global variables for better performance
recognizer = sr.Recognizer()
engine = pyttsx3.init() 
command_cache = {}  # Cache for frequent commands

# Configure speech engine for better performance
engine.setProperty('rate', 180)    # Faster speech speed
engine.setProperty('volume', 0.9)  # Volume level

# Pre-initialize pygame mixer for faster audio
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.mixer.init()

def speak_old(text):
    """Fast pyttsx3 speech without internet"""
    if not text or not text.strip():
        return
    try:
        print(f"🔊 Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {e}")

# Initialize pygame mixer once globally
pygame.mixer.init()

def speak(text):
    """Optimized speech function with caching and fast fallback"""
    if not text or not text.strip():
        return
    
    # Check cache for common responses
    if ENABLE_COMMAND_CACHE and text in command_cache:
        cached_response = command_cache[text]
        if time.time() - cached_response['timestamp'] < 300:  # 5 minutes cache
            print(f"🔊 Cached response: {text}")
            speak_old(text)
            return
    
    print(f"🔊 Speaking: {text}")
    
    if USE_OFFLINE_TTS:
        # Fast offline mode
        speak_old(text)
        return
    
    # Try gTTS with timeout and better error handling
    temp_file = "temp_speech.mp3"
    try:
        # Remove any existing temp file
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass
        
        # Create gTTS with timeout
        tts = gTTS(text=text, lang='en', slow=False, lang_check=False)
        tts.save(temp_file)
        
        # Load and play with timeout
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        
        # Wait for playback with timeout (max 10 seconds)
        start_time = time.time()
        while pygame.mixer.music.get_busy() and (time.time() - start_time) < 10:
            pygame.time.Clock().tick(10)
            
        # Clean up
        pygame.mixer.music.unload()
        
        # Remove temp file
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except:
            pass
            
        # Cache the response
        if ENABLE_COMMAND_CACHE:
            command_cache[text] = {'timestamp': time.time()}
        
        # Successfully played gTTS, so return to avoid fallback
        return
            
    except Exception as e:
        print(f"gTTS error: {e}")
        # Fast fallback to pyttsx3
        speak_old(text)
            
def launch_app(app_name):
    """Launch applications on Windows with expanded search capabilities"""
    app_commands = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "chrome": [r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", r"C:\Program Files\Google\Chrome\Application\chrome.exe", "chrome.exe"],
        "firefox": ["firefox.exe", r"C:\Program Files\Mozilla Firefox\firefox.exe", r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"],
        "edge": ["msedge.exe", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"],
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
        "task manager": "taskmgr.exe",
        "camera": "start microsoft.windows.camera:",
        "mail": "start outlookmail:",
        "maps": "start maps:",
        "calendar": "start outlookcal:",
        "store": "start ms-windows-store:",
        "sticky notes": "stikynot.exe",
        "snipping tool": "snippingtool.exe",
        "windows media player": "wmplayer.exe",
        "internet explorer": "iexplore.exe",
        "onedrive": "onedrive.exe",
        "onedrive personal": "onedrive.exe",
        "onedrive business": "odopen.exe"
    }
    
    app_name = app_name.lower().strip()
    
    if app_name in app_commands:
        command = app_commands[app_name]
        try:
            if isinstance(command, list):
                # Try multiple possible paths
                for cmd in command:
                    try:
                        if cmd.startswith("start "):
                            print(f"🔧 Executing system command: {cmd}")
                            os.system(cmd)
                            return True
                        elif cmd.startswith("C:\\"):
                            # Full path - check if file exists first
                            if os.path.exists(cmd):
                                print(f"🔍 Launching from path: {cmd}")
                                # Launch with visibility focus
                                subprocess.Popen([cmd], shell=False, creationflags=subprocess.CREATE_NEW_CONSOLE)
                                print(f"✅ Successfully launched {app_name} from {cmd}")
                                return True
                            else:
                                print(f"❌ Path not found: {cmd}")
                        else:
                            # Simple command - try to find in PATH
                            print(f"🔧 Trying simple command: {cmd}")
                            subprocess.Popen([cmd], shell=False)
                            print(f"✅ Successfully launched {app_name} with command: {cmd}")
                            return True
                    except Exception as e:
                        print(f"❌ Error launching {cmd}: {e}")
                        continue
                return False
            else:
                # Single command
                if command.startswith("start "):
                    # For special Windows protocols
                    print(f"🔧 Executing system command: {command}")
                    os.system(command)
                else:
                    # For regular applications
                    print(f"🔧 Launching with command: {command}")
                    subprocess.Popen([command], shell=False)
                    print(f"✅ Successfully launched {app_name}")
                return True
        except Exception as e:
            print(f"❌ Error launching {app_name}: {e}")
            return False
    else:
        # Try to find the app in common locations with broader search
        try:
            username = os.getlogin()
        except:
            # Fallback if os.getlogin() fails
            username = os.environ.get('USERNAME', 'default')
        
        # Common installation paths
        common_paths = [
            f"C:\\Program Files\\{app_name}\\{app_name}.exe",
            f"C:\\Program Files (x86)\\{app_name}\\{app_name}.exe",
            f"C:\\Users\\{username}\\AppData\\Local\\{app_name}\\{app_name}.exe",
            f"C:\\Users\\{username}\\AppData\\Roaming\\{app_name}\\{app_name}.exe",
        ]
        
        # Browser-specific paths
        if app_name == "chrome" or app_name == "google chrome":
            browser_paths = [
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                f"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"
            ]
            common_paths.extend(browser_paths)
        
        if app_name == "firefox" or app_name == "mozilla firefox":
            browser_paths = [
                r"C:\Program Files\Mozilla Firefox\firefox.exe",
                r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
            ]
            common_paths.extend(browser_paths)
        
        # Also try with common executable names
        common_executables = [
            "Application", "app", "App", "Main", "main", 
            app_name.replace(" ", ""),  # Remove spaces
            app_name.replace(" ", "").lower(),  # Remove spaces and lowercase
        ]
        
        for base_path in common_paths:
            # Replace {username} placeholder
            path = base_path.format(username=username)
            if os.path.exists(path):
                try:
                    print(f"🔍 Launching from path: {path}")
                    # Launch with visibility focus
                    subprocess.Popen([path], shell=False, creationflags=subprocess.CREATE_NEW_CONSOLE)
                    print(f"✅ Successfully launched {app_name} from {path}")
                    return True
                except Exception as e:
                    print(f"❌ Error launching from {path}: {e}")
        
        # Try alternative executable names in the directory
        for exec_name in common_executables:
            alt_path = f"C:\\Program Files\\{app_name}\\{exec_name}.exe"
            if os.path.exists(alt_path):
                try:
                    subprocess.Popen([alt_path])
                    return True
                except:
                    pass
                    
            alt_path = f"C:\\Program Files (x86)\\{app_name}\\{exec_name}.exe"
            if os.path.exists(alt_path):
                try:
                    subprocess.Popen([alt_path])
                    return True
                except:
                    pass
        
        # As a last resort, try Windows search
        try:
            # Try to launch using 'start' command which searches PATH
            result = subprocess.run(['start', app_name], shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return True
        except:
            pass
            
        # Try to find any .lnk or .exe file containing the app name
        search_dirs = [
            f"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs",
            f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs",
            "C:\\Program Files",
            "C:\\Program Files (x86)"
        ]
        
        for search_dir in search_dirs:
            if os.path.exists(search_dir):
                for root, dirs, files in os.walk(search_dir):
                    for file in files:
                        if app_name.replace(" ", "").lower() in file.replace(" ", "").lower():
                            if file.endswith(('.exe', '.lnk')):
                                try:
                                    full_path = os.path.join(root, file)
                                    subprocess.Popen([full_path])
                                    return True
                                except:
                                    continue
        
        return False

def search_youtube_video(query):
    """Search for a video on YouTube and open it"""
    try:
        # Clean up the query by removing common phrases
        cleaned_query = query.lower().strip()
        
        # Remove common command phrases
        for phrase in ["play", "on youtube", "youtube", "search", "find", "for", "can you"]:
            cleaned_query = cleaned_query.replace(phrase, "")
        
        cleaned_query = cleaned_query.strip()
        
        if not cleaned_query or cleaned_query == "":
            # If no specific query, just open YouTube homepage
            webbrowser.open("https://www.youtube.com/")
            return True
            
        # Create YouTube search URL
        search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(cleaned_query)}"
        
        # Open the search results
        webbrowser.open(search_url)
        return True
    except Exception as e:
        print(f"Error searching YouTube: {e}")
        return False

def aiProcess(command):
    """Process command using OpenAI with caching and timeout"""
    if OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
        return "Please configure your OpenAI API key in the code to use AI features."
    
    # Check cache first
    if ENABLE_COMMAND_CACHE and command in command_cache:
        cached_response = command_cache[command]
        if time.time() - cached_response['timestamp'] < 600:  # 10 minutes cache
            return cached_response['response']
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis. Give short, clear responses (max 20 words). Be helpful and friendly."},
                {"role": "user", "content": command}
            ],
            max_tokens=50,  # Reduced for faster responses
            timeout=10  # Add timeout
        )
        
        response = completion.choices[0].message.content
        
        # Cache the response
        if ENABLE_COMMAND_CACHE:
            command_cache[command] = {'response': response, 'timestamp': time.time()}
        
        return response
        
    except Exception as e:
        print(f"AI processing error: {e}")
        return "Sorry, I'm having trouble processing that request right now."

def processCommand(c):
    """Process voice commands with optimized handling"""
    command = c.lower().strip()
    
    # Check cache for common simple commands
    if ENABLE_COMMAND_CACHE and command in command_cache:
        cached = command_cache[command]
        if time.time() - cached['timestamp'] < 300:  # 5 minutes
            speak(cached['response'])
            return True
    
    # System commands (shutdown, restart, etc.)
    if "shutdown" in command or "shut down" in command:
        response = "Shutting down the computer in 10 seconds. Say 'cancel' to abort. Shutdown command disabled for safety. Enable manually if needed."
        if ENABLE_COMMAND_CACHE:
            command_cache[command] = {'response': response, 'timestamp': time.time()}
        speak(response)
        return True
    
    elif "restart" in command or "reboot" in command:
        response = "Restarting the computer in 10 seconds. Say 'cancel' to abort. Restart command disabled for safety. Enable manually if needed."
        if ENABLE_COMMAND_CACHE:
            command_cache[command] = {'response': response, 'timestamp': time.time()}
        speak(response)
        return True
    
    elif "sleep" in command or "hibernate" in command:
        response = "Putting computer to sleep. Sleep command disabled for safety. Enable manually if needed."
        if ENABLE_COMMAND_CACHE:
            command_cache[command] = {'response': response, 'timestamp': time.time()}
        speak(response)
        return True
    
    # Volume control commands
    elif "volume up" in command or "increase volume" in command:
        try:
            import ctypes
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            # Get current volume
            current_volume = volume.GetMasterVolumeLevelScalar()
            # Increase volume by 10%
            new_volume = min(current_volume + 0.1, 1.0)
            volume.SetMasterVolumeLevelScalar(new_volume, None)
            speak(f"Volume increased to {int(new_volume * 100)} percent")
        except:
            # Fallback using nircmd if pycaw is not available
            speak("Volume control not available. Please install pycaw module.")
        return True  # Continue running in main loop
    
    elif "volume down" in command or "decrease volume" in command:
        try:
            import ctypes
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            # Get current volume
            current_volume = volume.GetMasterVolumeLevelScalar()
            # Decrease volume by 10%
            new_volume = max(current_volume - 0.1, 0.0)
            volume.SetMasterVolumeLevelScalar(new_volume, None)
            speak(f"Volume decreased to {int(new_volume * 100)} percent")
        except:
            speak("Volume control not available. Please install pycaw module.")
        return True  # Continue running in main loop
    
    elif "mute" in command or "unmute" in command:
        try:
            import ctypes
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            # Toggle mute
            is_muted = volume.GetMute()
            volume.SetMute(not is_muted, None)
            if is_muted:
                speak("Unmuting audio")
            else:
                speak("Muting audio")
        except:
            speak("Mute/unmute not available. Please install pycaw module.")
        return True  # Continue running in main loop
    
    # YouTube video playing commands (enhanced patterns)
    if "play" in command and "youtube" in command:
        speak("Searching YouTube for your video")
        if search_youtube_video(command):
            speak("I've opened YouTube with your search results")
        else:
            speak("Sorry, I couldn't search YouTube right now")
        return True  # Continue running in main loop
        
    elif "search" in command and "youtube" in command:
        speak("Searching YouTube for your query")
        if search_youtube_video(command):
            speak("I've opened YouTube with your search results")
        else:
            speak("Sorry, I couldn't search YouTube right now")
        return True  # Continue running in main loop
    
    elif "youtube" in command and ("play" in command or "find" in command or "search" in command):
        speak("Searching YouTube for your video")
        if search_youtube_video(command):
            speak("I've opened YouTube with your search results")
        else:
            speak("Sorry, I couldn't search YouTube right now")
        return True  # Continue running in main loop
        
    elif command.startswith("youtube"):
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com/")
        return True  # Continue running in main loop
    
    elif "on youtube" in command and "play" in command:
        speak("Searching YouTube for your video")
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

def recognize_speech(recognizer, source, timeout=3, phrase_time_limit=2):
    """Helper function for speech recognition with retries"""
    for attempt in range(MAX_RETRIES):
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            return recognizer.recognize_google(audio, show_all=False)
        except sr.WaitTimeoutError:
            if attempt < MAX_RETRIES - 1:
                print(f"⏰ Timeout, retry {attempt + 1}/{MAX_RETRIES}...")
                continue
            else:
                raise
        except sr.UnknownValueError:
            if attempt < MAX_RETRIES - 1:
                print(f"🔇 Unrecognized speech, retry {attempt + 1}/{MAX_RETRIES}...")
                continue
            else:
                raise
        except sr.RequestError as e:
            if attempt < MAX_RETRIES - 1:
                print(f"📡 Network error, retry {attempt + 1}/{MAX_RETRIES}...")
                time.sleep(1)  # Wait before retry
                continue
            else:
                raise
    return None

def main():
    """Optimized main function with better error handling and performance"""
    print("🚀 Jarvis Virtual Assistant - Optimized Version")
    print("Features: Faster responses, caching, offline mode option")
    print("===============================================\n")
    
    # Initialize recognizer with optimized settings
    r = sr.Recognizer()
    r.energy_threshold = 300  # Lower threshold for better sensitivity
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.5   # Shorter pause for faster detection
    r.phrase_threshold = 0.2
    r.non_speaking_duration = 0.3
    
    # Configure microphone with timeout
    print("🔊 Initializing microphone...")
    try:
        with sr.Microphone() as source:
            print("🔊 Adjusting for ambient noise (1 second)...")
            r.adjust_for_ambient_noise(source, duration=1)
            print(f"🔊 Energy threshold: {r.energy_threshold}")
            print("✅ Microphone ready!\n")
    except Exception as e:
        print(f"❌ Microphone error: {e}")
        print("🔄 Running in text mode...")
        text_mode()
        return
    
    # Initialize with faster speech
    if USE_OFFLINE_TTS:
        speak_old("Jarvis initialized in fast offline mode")
    else:
        speak("Jarvis initialized with optimized settings")
    
    print("🎙️  Say 'Jarvis' to activate me")
    print("💡 Tip: Speak clearly and wait for activation prompt")
    if USE_OFFLINE_TTS:
        print("⚡ Fast mode: Using local text-to-speech")
    
    wake_word_timeout = 2.0  # Faster wake word detection
    command_timeout = 4.0    # Faster command processing
    
    while True:
        try:
            # Listen for wake word with timeout
            with sr.Microphone() as source:
                print("\n👂 Listening for 'Jarvis'...")
                
                try:
                    word = recognize_speech(r, source, timeout=wake_word_timeout, phrase_time_limit=1.5)
                    if word:
                        print(f"🔍 Detected: '{word}'")
                        
                        if "jarvis" in word.lower():
                            print("✅ Wake word detected!")
                            if USE_OFFLINE_TTS:
                                speak_old("Yes?")
                            else:
                                speak("Yes?")
                            print("📝 Listening for your command...")
                            
                            # Listen for command
                            try:
                                command = recognize_speech(r, source, timeout=command_timeout, phrase_time_limit=4)
                                if command:
                                    print(f"📝 Command: '{command}'")
                                    processCommand(command)
                                else:
                                    speak("I didn't catch that")
                            except (sr.UnknownValueError, sr.WaitTimeoutError):
                                speak("Please try again")
                            except sr.RequestError as e:
                                print(f"❌ Speech service error: {e}")
                                speak("Service temporarily unavailable")
                        else:
                            print(f"⏭️  Not wake word: '{word}'")
                            
                except sr.WaitTimeoutError:
                    print("⏰ Still listening...")
                    continue
                except sr.UnknownValueError:
                    print("🔇 No clear speech detected")
                    continue
                except sr.RequestError as e:
                    print(f"❌ Speech service error: {e}")
                    speak("Network service unavailable")
                    time.sleep(2)  # Wait before retry
                    
        except KeyboardInterrupt:
            print("\n\n👋 Jarvis shutting down...")
            speak("Goodbye")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            speak("System error occurred")
            time.sleep(1)

def text_mode():
    """Text-based mode for testing and fallback"""
    print("\n📝 Text Mode - Type your commands")
    print("Commands: 'quit', 'exit', or Ctrl+C to exit")
    
    while True:
        try:
            command = input("\n📝 You: ").strip()
            if command.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("👋 Goodbye!")
                break
            
            if command:
                processCommand(command)
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def toggle_offline_mode():
    """Toggle between online and offline TTS modes"""
    global USE_OFFLINE_TTS
    USE_OFFLINE_TTS = not USE_OFFLINE_TTS
    mode = "offline (fast)" if USE_OFFLINE_TTS else "online (quality)"
    print(f"🔄 TTS mode changed to: {mode}")
    speak(f"TTS mode set to {mode}")

if __name__ == "__main__":
    # Handle command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "text":
            text_mode()
        elif sys.argv[1] == "offline":
            USE_OFFLINE_TTS = True
            main()
        elif sys.argv[1] == "online":
            USE_OFFLINE_TTS = False
            main()
        else:
            print("Usage: python main.py [text|offline|online]")
            print("  text    - Run in text mode")
            print("  offline - Use fast pyttsx3 only (no internet)")
            print("  online  - Use gTTS with fallback (default)")
    else:
        main()