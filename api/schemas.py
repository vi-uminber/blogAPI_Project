
from bson import ObjectId

from pydantic import BaseModel, Field, EmailStr, root_validator
import os





 




# Load environment variables
# load_dotenv()
# uri = os.getenv("://Vicky:p3GXCqjaYyPv8ZZl@cluster0.xlayhr6.mongodb.net/blog_api?retryWrites=true&w=majority&appName=Cluster0")  # Assuming you have MONGODB_URI in your .env

# # Create a new client and connect to the server
# db = MongoClient(uri, server_api=ServerApi('1'))

# # Send a ping to confirm a successful connection
# try:
#     db.admin.command('ping')
#     print("*****************************")
#     print("Pinged your deployment. You successfully connected to MongoDB!")
#     print("*****************************")
# except Exception as e:
#     print("*****************************")
#     print(e)
#     print("*****************************")

# class ObjectIdStr(str):
#     @classmethod
#     def __get_validators__(cls):
#         yield validate_object_id

# def validate_object_id(value):
#     if not ObjectId.is_valid(value):
#         raise ValueError("Invalid ObjectId")
#     return ObjectId(value)





class UserCreate(BaseModel):
    # id: ObjectIdStr = Field(..., alias="_id", validate_object_id=validate_object_id)
    id: str = Field(...)
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "23ghj786tyruv",
                "name": "John Doe",
                "email": "jdoe@example.com",
                "password": "secret_code"
            }
        }

# class UserResponse(BaseModel):
#     # id: ObjectIdStr = Field(..., alias="_id", validate_object_id=validate_object_id)
#     name: str = Field(...)
#     email: EmailStr = Field(...)

#     class Config:
#         populate_by_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
#         schema_extra = {
#             "example": {
#                 "id": "507f191e810c19729de860ea",
#                 "name": "John Doe",
#                 "email": "jdoe@example.com"
#             }
#         }

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    apiKey: str 
    
schema_extra = {
            "example":{
                "name": "John Doe",
                "email": "jdoe@gmail.com"
                
        }
    } 


class TokenData(BaseModel):
    id: str
    
class PasswordReset(BaseModel):
    email: EmailStr
    
class NewPassword(BaseModel):
    password: str
    
    
class BlogContent(BaseModel):
    # id: str
    title: str=Field(...)
    body: str=Field(...)
    
    
    class Config:
        schema_extra = {
            "example":{
                "title": "Blog title",
                "body": "Blog Content"
                
        }
    } 
    
class BlogContentResponse(BaseModel):
    title: str=Field(...)
    body: str=Field(...)
    author_name: str=Field(...)
    author_id:str=Field(...)
    created_at: str=Field(...)
    
    
    class Config:
        schema_extra = {
            "example":{
                "title": "Blog title",
                "body": "Blog Content",
                "author_name": "name of the author",
                "author_id": "ID of the author",
                "created_at": "date create"
                
        }
    } 