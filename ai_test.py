import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input="What is the day today?",
    tools=[{"type": "google_search"}]
)

print(interaction.output_text)
