from passlib.context import CryptContext
import logging


pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def authenticate_user(name: str, password: str, user_collection):
    user = await user_collection.find_one({"name": name.lower()})
    if user is None:
        logging.debug(f"User not found for username: {name}")
        return False
    if not verify_password(password, user["password"]):
        logging.debug(f"Password verification failed for user: {name}")
        return False
    logging.debug(f"User authenticated successfully: {name}")
    return user