from google import genai
import os
from dotenv import load_dotenv

# Load your API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API Key not found in .env file!")
    exit()

client = genai.Client(api_key=api_key)

print("Fetching available models...\n")

# Simply list the name of every model available to your API key
for model in client.models.list():
    print(f"Model Name: {model.name}")