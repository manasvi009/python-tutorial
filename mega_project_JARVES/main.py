import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

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
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        if NEWS_API_KEY == "YOUR_NEWS_API_KEY_HERE":
            speak("Please configure your NewsAPI key to get news updates.")
            return
            
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

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 





if __name__ == "__main__":
    # Initialize recognizer
    r = sr.Recognizer()
    
    # Configure microphone settings
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait.")
            r.adjust_for_ambient_noise(source, duration=1)
            print("Microphone calibrated!")
    except Exception as e:
        print(f"Microphone setup error: {e}")
        print("Make sure you have a working microphone connected.")
    
    speak("Initializing Jarvis....")
    print("Jarvis is ready! Say 'Jarvis' to activate me.")
    
    while True:
        try:
            # Listen for the wake word "Jarvis"
            with sr.Microphone() as source:
                print("Listening for wake word...")
                # Longer timeout for wake word detection
                audio = r.listen(source, timeout=3, phrase_time_limit=2)
            
            word = r.recognize_google(audio)
            print(f"Heard: {word}")
            
            if word.lower() == "jarvis":
                speak("Yes, how can I help you?")
                print("Jarvis activated! Listening for command...")
                
                # Listen for command
                with sr.Microphone() as source:
                    print("Listening for your command...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    command = r.recognize_google(audio)
                    print(f"Command received: {command}")
                    
                    processCommand(command)
            
        except sr.WaitTimeoutError:
            # This is normal - just continue listening
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