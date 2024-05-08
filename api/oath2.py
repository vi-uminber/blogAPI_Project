from jose import jwt , JWTError
from datetime import datetime, timedelta
from .schemas import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer 
from .database import get_database as db  
import os 
from dotenv import load_dotenv

from api import utils
from api.database import get_database
from api.utils import verify_password
from bson import ObjectId
print("Successfully imported!")


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

SECRET_KEY= os.getenv("SECRET_KEY")
ALGORITHM= os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUITES= int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUITES", "60"))

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="/login") # for get current user and it is useing in get current user function 


def create_access_token(payload:dict, expires_delta: timedelta):
    to_encode = payload.copy()
    
    expiration_time = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expiration_time})
    
    
    
    jw_token = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return jw_token




# def verify_access_token(token: str, credential_exception):
#     try:
#         payload= jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        
#         id: str = payload.get("id")
#         exp = payload.get("exp")
        
#         if not id:
#             raise credential_exception
        
#         # Convert exp to datetime object
#         expiration_time = datetime.fromtimestamp(exp)
        
#         if expiration_time < datetime.utcnow():
#             raise credential_exception
        
#         token_data = TokenData(id=id)
#         return token_data
    
#     except JWTError:
#         raise credential_exception

def verify_access_token(token: str, credential_exception):
    try:
        print(f"SECRET_KEY: {SECRET_KEY}") 
        print(f"ALGORITHM: {ALGORITHM}")
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded payload: {payload}")
        user_id: str = payload.get("id")
        if not user_id:
            raise credential_exception
        expiration_time = datetime.fromtimestamp(payload["exp"])
        if datetime.utcnow() > expiration_time:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        return TokenData(id=user_id)
    except JWTError as e:
        print(f"JWT Error: {e}")  # Log the specific JWT error
        raise credential_exception

    


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     db = get_database()
#     collection = db["users"]
#     try:
#         payload = verify_access_token(token, HTTPException(
#             status_code=401,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"}))
#         user_id = payload.id
#         if ObjectId.is_valid(user_id):
#             user_id = ObjectId(user_id)
#         else:
#             raise HTTPException(status_code=404, detail="Invalid user ID format")

#         user = await collection.find_one({"_id": user_id})
#         if user is None:
#             raise HTTPException(status_code=404, detail="User not found")
#         return user
#     except HTTPException as e:
#         raise e

async def get_current_user(token: str = Depends(oauth2_scheme)):
    print(f"Received token: {token}")
    db = get_database()
    collection = db["users"]
    try:
        payload = verify_access_token(token, HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}))
        user_id = payload.id
        
         # Convert user_id string to ObjectId
        if ObjectId.is_valid(user_id): 
            user_id = ObjectId(user_id)  
        else:
            raise HTTPException(status_code=404, detail="Invalid user ID format")

        user = await collection.find_one({"_id": user_id})
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except HTTPException as e:
        raise e
    










