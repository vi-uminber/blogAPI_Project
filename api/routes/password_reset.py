from urllib import request
from fastapi import APIRouter, Depends, Request
from ..schemas import PasswordReset, NewPassword
from ..oath2 import create_access_token, get_current_user
from fastapi import HTTPException, status
from ..send_email import password_reset
from ..database import get_database
from datetime import timedelta
from ..utils import get_password_hash
from api import utils

router = APIRouter(
    prefix="/password",
    tags=["Password reset"]
)


@router.post("", response_description="Reset Password")
async def reset_request(user_email: PasswordReset):
    db = get_database()
    collection = db["users"]
    user = await collection.find_one({"email": user_email.email})
    
    if user is not None:
        token = create_access_token({"id": str(user["_id"])}, expires_delta=timedelta(minutes=30))
        
        reset_link = f"http://localhost:8000/reset?token={token}"
        
        #TODO: send email
        await password_reset("Password Reset", user["email"],{
            "title": "password_reset",
            "name": user["name"],
            "reset_link": reset_link
            
        } )
        
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email not found" 
        )
        


@router.put("", response_description="Reset password")
async def reset(token: str, new_password: NewPassword):
    db = get_database()
    collection = db["users"]
    user = await get_current_user(token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not new_password.password:
        raise HTTPException(status_code=400, detail="Password is required")

    hashed_password = get_password_hash(new_password.password)
    update_result = await collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"password": hashed_password}}
    )
    
    if update_result.modified_count == 0:
        raise HTTPException(
            status_code=400, detail="Update failed"
        )
    
    return {"message": "Password updated successfully"}