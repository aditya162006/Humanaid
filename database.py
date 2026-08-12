import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")
if not TURSO_DATABASE_URL or not TURSO_AUTH_TOKEN:
    raise RuntimeError("Turso credentials not set in environment!")
engine = create_engine(
    f"sqlite+{TURSO_DATABASE_URL}?secure=true",
    connect_args={
        "auth_token": TURSO_AUTH_TOKEN,
    },
)
