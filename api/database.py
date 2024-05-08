from motor.motor_asyncio import AsyncIOMotorClient
import os

client: AsyncIOMotorClient = None

def get_database():
    global client
    if client is None:
        raise Exception("MongoDB client not initialized")
    return client["blog_api"]

def create_mongo_connection():
    MONGO_URL = os.getenv("MONGODB_URI")
    if not MONGO_URL:
        raise Exception("MongoDB URI not found in environment variables")
    global client
    client = AsyncIOMotorClient(MONGO_URL)

def close_mongo_connection():
    global client
    if client:
        client.close()  
