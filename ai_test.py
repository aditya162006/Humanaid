import os
from dotenv import load_dotenv
from exa_py import Exa

load_dotenv()

exa = Exa(api_key=os.getenv("EXA_API_KEY"))

results = exa.search(
    "latest humanitarian developments in Sudan",
    num_results=5,
    contents={
        "highlights": True
    }
)

for result in results.results:
    print("=" * 80)
    print("TITLE:", result.title)
    print("URL:", result.url)

    if result.highlights:
        print("CONTENT:")
        print("\n".join(result.highlights))
