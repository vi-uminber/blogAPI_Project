from fastapi import FastAPI
from .database import create_mongo_connection, close_mongo_connection, get_database
from .routes import users, auth, password_reset, blog_content
from dotenv import load_dotenv
import os 


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

print("Loaded MongoDB URI:", os.getenv("MONGODB_URI"))

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    create_mongo_connection()

@app.on_event("shutdown")
async def shutdown_event():
    close_mongo_connection()    

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(password_reset.router)
app.include_router(blog_content.router)