from fastapi import APIRouter, Depends,status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..database import get_database
from .. import utils 
from ..oath2 import ACCESS_TOKEN_EXPIRE_MINUITES, create_access_token
from dotenv import load_dotenv
import os 
from datetime import datetime, timedelta

from ..utils import verify_password,  authenticate_user
from datetime import datetime, timedelta

import logging




router= APIRouter(
    prefix="/login",
    tags=["Authentication"]
)



# async def authenticate_user(name: str, password: str, user_collection):
#     user = await user_collection.find_one({"name": name.lower()})
#     if user is None:
#         logging.debug(f"User not found for username: {name}")
#         return False
#     if not verify_password(password, user["password"]):
#         logging.debug(f"Password verification failed for user: {name}")
#         return False
#     logging.debug(f"User authenticated successfully: {name}")
#     return user

# @router.post("", response_model=dict)
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     db = get_database()
#     user_collection = db["users"]  # Retrieve the actual collection object
#     user = await authenticate_user(form_data.username, form_data.password, user_collection)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
#     access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUITES))
#     access_token = create_access_token(
#         payload={"sub": user["name"]},  # Include any required claims here
#         expires_delta=access_token_expires
#     )
    
#     return {
#         "access_token": access_token,
#         "token_type": "bearer"
#     }

@router.post("", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_database()
    user_collection = db["users"]
    user = await authenticate_user(form_data.username, form_data.password, user_collection)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUITES)
    access_token = create_access_token(
        payload={"id": str(user["_id"]), "sub": user["name"]},  # Include user ID in payload
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
