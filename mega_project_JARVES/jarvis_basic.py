import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import pygame
import os
import time
import subprocess
import platform

# Configuration
recognizer = sr.Recognizer()
engine = pyttsx3.init() 

# Configure speech engine
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

# Initialize pygame mixer
pygame.mixer.init()

def speak(text):
    """Convert text to speech"""
    if not text or not text.strip():
        return
        
    print(f"Speaking: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {e}")

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

def processCommand(c):
    """Process voice commands without API keys"""
    command = c.lower()
    
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
    
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
        
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
        
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
        
    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
        
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
            
    elif "hello" in command or "hi" in command:
        speak("Hello! How can I help you today?")
        
    elif "how are you" in command:
        speak("I'm doing great, thank you for asking!")
        
    elif "what time" in command:
        import datetime
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
        
    elif "what day" in command or "what date" in command:
        import datetime
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {today}")
        
    elif "thank you" in command or "thanks" in command:
        speak("You're welcome!")
        
    elif "bye" in command or "goodbye" in command:
        speak("Goodbye! Have a great day!")
        return False  # Signal to exit
        
    else:
        speak("I can help you with: opening websites, launching applications, playing music, telling time, or having a simple conversation. Try saying 'open notepad' or 'launch calculator'. What would you like me to do?")
    
    return True  # Continue running

def main():
    """Main function to run the assistant"""
    print("=== Jarvis Virtual Assistant ===")
    print("Features available without API keys:")
    print("- Web browsing (Google, Facebook, YouTube, LinkedIn)")
    print("- Application launching (Notepad, Calculator, Chrome, etc.)")
    print("- Music playback")
    print("- Basic conversation")
    print("- Time and date")
    print("===============================")
    
    # Test microphone setup
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Microphone ready!")
    except Exception as e:
        print(f"Microphone setup error: {e}")
        print("Running in text mode instead...")
        text_mode()
        return
    
    speak("Hello! I'm Jarvis. Say my name to activate me.")
    print("Say 'Jarvis' to activate, or say 'bye' to exit.")
    
    running = True
    while running:
        try:
            with sr.Microphone() as source:
                print("\nListening for 'Jarvis'...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
            
            word = recognizer.recognize_google(audio)
            print(f"Heard: {word}")
            
            if word.lower() == "jarvis":
                speak("Yes, how can I help you?")
                print("Listening for your command...")
                
                with sr.Microphone() as source:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    print(f"Command: {command}")
                    
                    running = processCommand(command)
            
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