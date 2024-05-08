from fastapi import APIRouter, HTTPException, Depends
from ..schemas import UserCreate, UserResponse
from ..utils import get_password_hash
from ..database import get_database
import secrets
from ..send_email import send_registration_mail




router = APIRouter(
    tags=["Users Routes"]
)


@router.post("/registration", response_model=UserResponse)
async def register_user(user: UserCreate):
    db = get_database()
    collection = db["users"]
    existing_user = await collection.find_one({"email": user.email})
    existing_name = await collection.find_one({"name": user.name})
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if existing_name:
        raise HTTPException(status_code=400, detail="username already registered")
    
    hashed_password = get_password_hash(user.password)
    api_key = secrets.token_hex(16)
    user_data = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "apiKey": api_key
        
    }
    
    result = await collection.insert_one(user_data)
    new_user_id = result.inserted_id
    user_data.pop('password')  # Remove password for security reasons
    user_data['id'] = str(new_user_id)
    
    await send_registration_mail("Registration Succesfull", user_data["email"], {
        "title": "Registration Succesfull",
        "name": user_data["name"]
        
    })
    
    return user_data
    
    
    

    
    
