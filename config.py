import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
    CHANNEL_1 = os.getenv("CHANNEL_1", "")
    CHANNEL_2 = os.getenv("CHANNEL_2", "")
    STORAGE_CHANNEL_ID = os.getenv("STORAGE_CHANNEL_ID", "")
    
    # Bot Username (Will be fetched at runtime if empty, but good for links)
    BOT_USERNAME = os.getenv("BOT_USERNAME", "") 
    
    # Database Path
    DB_PATH = "data/database.db"

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
