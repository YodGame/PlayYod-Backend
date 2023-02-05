from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ORIGINS = [
    "http://localhost",
    "http://localhost:3000"
]

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_COLLECTION = "PlayYod"
