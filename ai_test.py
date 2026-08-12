import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

response = client.models.generate_content(
    model="gemini-3.5-flash",  # Or "gemini-3.6-flash" / "gemini-flash-latest"
    contents="Explain the humanitarian crisis in Sudan in 100 words."
)

print(response.text)
