# Voice Recognition Troubleshooting Guide

## 🎤 Improving Voice Recognition Accuracy

### ✅ What's Been Improved:
- **Better energy threshold**: Automatically adjusted to your environment
- **Extended listening time**: More time to detect your voice
- **Enhanced error handling**: Clear feedback when speech isn't understood
- **Visual feedback**: Emoji indicators show what's happening

### 🔧 Tips for Better Recognition:

#### 1. **Speaking Technique**
- Speak clearly at a normal volume
- Pause slightly between words
- Don't speak too quickly
- Enunciate the wake word "Jarvis" clearly

#### 2. **Environment**
- Use in a quiet room when possible
- Avoid background noise (fans, music, TV)
- Close doors/windows if there's street noise
- Position microphone away from speakers

#### 3. **Microphone Settings**
- Make sure your microphone is selected as default input device
- Check microphone volume in Windows settings (70-80% recommended)
- Test your microphone in Windows sound settings first

#### 4. **Command Structure**
- **Wake word**: "Jarvis" (clearly pronounced)
- **Wait for response**: Listen for "Yes, how can I help you?"
- **Give command**: Speak your request clearly
- **Examples**: 
  - "open notepad"
  - "launch calculator" 
  - "what time is it"

### 🛠️ If Still Having Issues:

#### Check Microphone Access:
1. Go to Windows Settings → Privacy → Microphone
2. Make sure "Allow apps to access your microphone" is ON
3. Ensure Python/Jarvis has permission

#### Test Your Microphone:
```bash
python test_microphone.py
```

#### Adjust Sensitivity Manually:
In the code, you can modify:
```python
recognizer.energy_threshold = 400  # Try 300-500 range
recognizer.pause_threshold = 0.8   # Try 0.5-1.0 range
```

#### Alternative: Use Text Mode
If voice recognition continues to be problematic:
```bash
python jarvis_basic.py
# When it fails to detect microphone, it will switch to text mode automatically
```

### 📊 Status Indicators:
- 👂 Listening for wake word
- 🔍 Heard: '[word]' - Shows what was detected
- ✅ Jarvis activated - Wake word recognized
- 📝 Command received - Processing your request
- ❌ Could not understand - Try speaking more clearly
- ⏰ Still listening - Normal timeout, continuing to listen

The system now provides much better feedback about what's happening during voice recognition!