from openai import OpenAI

# Configuration - Update with your actual API key
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY_HERE"  # Replace with your OpenAI API key

if OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
    print("Please configure your OpenAI API key in client.py")
    exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)