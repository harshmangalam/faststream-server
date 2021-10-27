import os

PORT = os.getenv("PORT", 4000)
HOST = os.getenv("HOST", "0.0.0.0")
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///faststream.db")
STATIC_PATH = os.getenv("STATIC_PATH", "static")


ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "8212622d28b52e2baf15e75b9252afc311ab76467f60dcacd7d731afebb67c47"
ALGORITHM = "HS256"


ORIGINS = [
    "http://localhost:3000",
]
