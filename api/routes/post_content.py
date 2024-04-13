from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ..utilities import utils
from ..schemas import PostContent, PostContentResponse
from .. import oauth2

router = APIRouter(
    prefix="/content",
    tags=["Post Content"]
)

@router.post("", response_description="Create post content")
async def create_post(post_content: PostContent, current_user = Depends(oauth2.get_current_user)):
    try:
        post_content_Object = jsonable_encoder(post_content)
        post_owner = f"{current_user["last_name"]} {current_user["first_name"]}"    
        post_content_Object["post_owner"] = post_owner
        post_content_Object["user_email"] = current_user["email"]

        new_post = await utils.db["post_contents"].insert_one(post_content_Object)
        return ({"message": "Post was successfully created."})
    
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )
    
@router.get("", response_description="Get post content", response_model=List[PostContentResponse])
async def get_posts(limit: int = 10, orderby: str = "creation_date"):
    try:
        post_content = await utils.db["post_contents"].find({"$query": {}, "$orderby": {orderby: -1}}).to_list(limit)
        return post_content

    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )
    
@router.get("/{id}", response_description="Get single post content", response_model=PostContentResponse)
async def get_posts(id: str):
    try:
        post_content = await utils.db["post_contents"].find_one({"_id": id})
        if post_content is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)
        return post_content

    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )

@router.put("", response_description="modify post content")
async def update_post(id: str, post_content: PostContent, current_user = Depends(oauth2.get_current_user)):
    try:
        if blog_post := await utils.db["post_contents"].find_one({"_id": id}):
            if blog_post["user_email"] != current_user["email"]:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="You are not the owner of this post."
                )
            
        post_content = {k: v for k, v in post_content.dict().items() if v is not None}
        if len(post_content) >= 1:
            update_result = await utils.db["post_contents"].update_one({"_id": id}, {"$set": post_content})
            if update_result.modified_count == 1:
                return ({"message": "Post was successfully modified."})
    
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )

@router.delete("/{id}", response_description="Delete single post content")
async def delete_posts(id: str, current_user = Depends(oauth2.get_current_user)):
    try:
        if blog_post := await utils.db["post_contents"].find_one({"_id": id}):
            if blog_post["user_email"] != current_user["email"]:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="You are not the owner of this post."
                )
        delete_result = await utils.db["post_contents"].delete_one({"_id": id})    
        if delete_result.deleted_count == 1:
            return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this post does not exist.")
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="network issue. please try again."
        )
