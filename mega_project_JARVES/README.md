# Jarvis Virtual Assistant

A Python-based virtual assistant that can perform various tasks through voice commands.

## Features
- Voice recognition and text-to-speech
- Web browsing (Google, Facebook, YouTube, LinkedIn)
- Music playback from predefined library
- News updates
- AI-powered responses using OpenAI GPT

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
You need to get API keys for the following services:

#### OpenAI API Key (Required for AI features)
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to API Keys section
4. Create a new secret key
5. Copy the key and replace `YOUR_OPENAI_API_KEY_HERE` in:
   - `main.py` (line 18)
   - `client.py` (line 4)

#### NewsAPI Key (Required for news feature)
1. Go to [NewsAPI](https://newsapi.org/)
2. Sign up for a free account
3. Get your API key
4. Replace `YOUR_NEWS_API_KEY_HERE` in `main.py` (line 19)

### 3. Test Your Setup
Run the microphone test:
```bash
python test_microphone.py
```

### 4. Run the Assistant
```bash
python main.py
```

## How to Use

1. Run the program
2. Say "Jarvis" to activate the assistant
3. Wait for the response "Yes, how can I help you?"
4. Give your command, for example:
   - "open google"
   - "play stealth" 
   - "what is the weather"
   - "news"

## Available Commands

### Web Browsing
- "open google"
- "open facebook"
- "open youtube"
- "open linkedin"

### Music
- "play stealth"
- "play march"
- "play skyfall"
- "play wolf"

### News
- "news" - Get latest headlines

### AI Assistant
- Any other query will be processed by OpenAI

## Troubleshooting

### Microphone Issues
- Make sure your microphone is connected and working
- Check microphone permissions in Windows settings
- Run `test_microphone.py` to diagnose issues

### API Key Errors
- Ensure you've replaced the placeholder keys with actual API keys
- Check your internet connection
- Verify API key limits haven't been exceeded

### Audio Issues
- Make sure your speakers/headphones are working
- Check Windows audio settings
- Try adjusting microphone sensitivity

## Files
- `main.py` - Main assistant program
- `client.py` - OpenAI API test script
- `musicLibrary.py` - Music links configuration
- `test_microphone.py` - Microphone testing tool
- `requirements.txt` - Python dependencies

## Requirements
- Python 3.7+
- Working microphone
- Internet connection
- API keys for OpenAI and NewsAPI