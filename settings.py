from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "https://playyod.maxnus.com"
]

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_COLLECTION = "PlayYod"

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_TOKEN_EXPIRE_MINUTES = 30
