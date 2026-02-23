import speech_recognition as sr

def test_microphone():
    """Test if microphone is working properly"""
    print("Testing microphone...")
    
    recognizer = sr.Recognizer()
    
    try:
        # List available microphones
        print("Available microphones:")
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"  {index}: {name}")
        
        # Test with default microphone
        with sr.Microphone() as source:
            print("\nAdjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Please say something...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            
        print("Processing audio...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        print("✅ Microphone test successful!")
        return True
        
    except sr.WaitTimeoutError:
        print("❌ Timeout: No speech detected")
        return False
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        return False
    except sr.RequestError as e:
        print(f"❌ Speech recognition service error: {e}")
        return False
    except Exception as e:
        print(f"❌ Microphone error: {e}")
        return False

if __name__ == "__main__":
    test_microphone()