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
    
    # Try gTTS first (actual speech output) with better error handling
    temp_file = "temp_speech.mp3"
    try:
        # Remove any existing temp file
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass  # Ignore if can't remove
        
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
        
        # Remove temp file after use
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except:
            pass  # Ignore cleanup errors
            
    except Exception as e:
        print(f"gTTS error: {e}")
        # Fallback to pyttsx3
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e2:
            print(f"Fallback speech also failed: {e2}")

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

def processCommand(c):
    """Process voice commands without API keys"""
    command = c.lower()
    
    # System commands (shutdown, restart, etc.)
    if "shutdown" in command or "shut down" in command:
        speak("Shutting down the computer in 10 seconds. Say 'cancel' to abort.")
        # For safety, I won't actually execute shutdown here
        # os.system("shutdown /s /t 10")  # Uncomment to enable
        speak("Shutdown command disabled for safety. Enable manually if needed.")
        return True
    
    elif "restart" in command or "reboot" in command:
        speak("Restarting the computer in 10 seconds. Say 'cancel' to abort.")
        # For safety, I won't actually execute restart here
        # os.system("shutdown /r /t 10")  # Uncomment to enable
        speak("Restart command disabled for safety. Enable manually if needed.")
        return True
    
    elif "sleep" in command or "hibernate" in command:
        speak("Putting computer to sleep.")
        # os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")  # Uncomment to enable
        speak("Sleep command disabled for safety. Enable manually if needed.")
        return True
    
    # Volume control commands
    elif "volume up" in command or "increase volume" in command:
        import ctypes
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        
        try:
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
        return True
    
    elif "volume down" in command or "decrease volume" in command:
        import ctypes
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        
        try:
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
        return True
    
    elif "mute" in command or "unmute" in command:
        import ctypes
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        
        try:
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
        return True
    
    # YouTube video playing commands (enhanced patterns)
    if "play" in command and "youtube" in command:
        speak("Searching YouTube for your video")
        if search_youtube_video(command):
            speak("I've opened YouTube with your search results")
        else:
            speak("Sorry, I couldn't search YouTube right now")
        return True
        
    elif "search" in command and "youtube" in command:
        speak("Searching YouTube for your query")
        if search_youtube_video(command):
            speak("I've opened YouTube with your search results")
        else:
            speak("Sorry, I couldn't search YouTube right now")
        return True
    
    elif "youtube" in command and ("play" in command or "find" in command or "search" in command):
        speak("Searching YouTube for your video")
        if search_youtube_video(command):
            speak("I've opened YouTube with your search results")
        else:
            speak("Sorry, I couldn't search YouTube right now")
        return True
        
    elif command.startswith("youtube"):
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com/")
        return True
    
    elif "on youtube" in command and "play" in command:
        speak("Searching YouTube for your video")
        if search_youtube_video(command):
            speak("I've opened YouTube with your search results")
        else:
            speak("Sorry, I couldn't search YouTube right now")
        return True
    
    # Web browsing commands (prioritized over app launching to avoid confusion)
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
        return True
        
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
        return True
        
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
        return True
        
    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
        return True
    
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
        return True
    
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
        speak("I can help you with: opening websites, launching applications, playing music, searching YouTube, controlling volume, managing system tasks, telling time, or having a simple conversation. Try saying 'open notepad' or 'search YouTube for tutorials'. What would you like me to do?")
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
    
    # Try microphone first, but if it fails, run in text mode
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
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "text":
        text_mode()
    else:
        main()