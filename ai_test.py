import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model= "gemini-2.5-flash",
    contents="Explain About World War 2 in 200 words.")
print(response.text)
