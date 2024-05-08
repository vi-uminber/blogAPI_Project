from fastapi import APIRouter, Depends,HTTPException, status

from api.database import get_database
from ..schemas import BlogContent, BlogContentResponse
from ..oath2 import get_current_user
from fastapi.encoders import jsonable_encoder
from datetime import timedelta, datetime
from typing import List
from bson import ObjectId



router = APIRouter(
    prefix="/blog",
    tags=["Blog Content"]
)


@router.post("", response_description="Create blog content", response_model=BlogContentResponse)
async def create_blog(blog_content: BlogContent, current_user=Depends(get_current_user)):
    db = get_database()
    collection = db["blogPost"]
    try:
        blog_content_data = blog_content.dict()
        blog_content_data["author_name"] = current_user["name"]
        blog_content_data["author_id"] = str(current_user["_id"])  # Convert to string if not already
        blog_content_data["created_at"] = str(datetime.utcnow())
        
        new_blog_content = await collection.insert_one(blog_content_data)
        created_blog_post = await collection.find_one({"_id": new_blog_content.inserted_id})
        
        return created_blog_post
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("", response_description="Get blog content", response_model=List[BlogContentResponse])

async def get_blogs(limit: int = 4, orderby: str = "created_at"):

    db = get_database()
    collection = db["blogPost"]
    try:
        blog_posts = await collection.find({"$query": {}, "$orderby": {orderby: -1}}).to_list(limit)
        return blog_posts
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
        
@router.get("/{id}", response_description="Get blog content by ID", response_model=BlogContentResponse)
async def get_blog(id: str):
    try:
        object_id = ObjectId(id)  # Convert the string id to ObjectId
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID format"
        )

    db = get_database()
    collection = db["blogPost"]
    try:
        blog_post = await collection.find_one({"_id": object_id})
        if blog_post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog with this id not found"
            )
        
        return blog_post
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
        
        


@router.put("/{id}", response_description="Update blog content", response_model=BlogContentResponse)
async def update_blog(id: str, blog_content: BlogContent, current_user=Depends(get_current_user)):

    db = get_database()
    collection = db["blogPost"]
        
    if blog_post := await collection.find_one({"_id": ObjectId(id)}):
        
        if blog_post["author_id"] == str(current_user["_id"]):
            
            try:
                blog_content = {k: v for k, v in blog_content.dict().items() if v is not None}
                
                if len(blog_content) >= 1:
                    update_result = await collection.update_one({"_id": ObjectId(id)}, {"$set": blog_content})
                    if update_result.modified_count == 1:
                        if (updated_blog_post := await collection.find_one({"_id": ObjectId(id)})) is not None:
                            return updated_blog_post
                
                if (existing_post := await collection.find_one({"_id": ObjectId(id)})) is not None:
                    return existing_post
                
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Blog content not found"
                )
                
                
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error"
                )
    
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="You are not the author of this blog post"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Blog content not found"
        )
        


@router.delete("/{id}", response_description="Delete blog post")
async def delete_blog_post(id: str, current_user=Depends(get_current_user)):
    db = get_database()
    collection = db["blogPost"]
    
    if blog_post := await collection.find_one({"_id": ObjectId(id)}):
        if blog_post["author_id"] == str(current_user["_id"]):
        
            try:
                delete_result = await collection.delete_one({"_id": ObjectId(id)})
            
                if delete_result.deleted_count == 1:
                    return HTTPException(
                        status_code=status.HTTP_204_NO_CONTENT
                    )
                
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error"
                )
            
            
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error"
                )
    
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not the author of this blog post"
            )
          
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog content not found"
        )
    
    

        