# Database configuration and connection setup
# app/database.py
# app/database.py
import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.get_database()  # Uses "mcq_generator" from the URI
