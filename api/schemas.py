from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value, field):
        if not ObjectId.is_valid(value):
            raise ValueError('Invalid ObjectId')
        return str(value)

    @classmethod
    def __get_pydantic_field_info__(cls):
        return {"type": "string"}
    

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    first_name: str
    last_name: str
    profile_picture: str = None
    cover_photo: str = None
    password: str
    is_active: bool = True
    is_email_verified: bool = False
    is_mobile_verified: bool = False
    creation_date: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "first_name": "Samson",
                "last_name": "John",
                "email": "sammy@gmail.com",
                "password": "zA@322445&^"
            }
        }

class UserResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    first_name: str
    last_name: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "first_name": "Samson",
                "last_name": "John",
                "email": "sammy@gmail.com"
            }
        }

class TokenData(BaseModel):
    id: str

class CompleteUserRegistration(BaseModel):
    email: str
    otp: str

class PasswordReset(BaseModel):
    email: str

class CompletePasswordReset(BaseModel):
    email: str
    otp: str
    new_password: str

class PostContent(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_email: str = None
    post_owner: str = None
    content: str
    media_url: str
    creation_date: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "content": "enter more details here",
                "media_url": ""
            }
        }

class PostContentResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_email: str = None
    post_owner: str = None
    content: str
    media_url: str
    creation_date: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "content": "enter more details here",
                "media_url": ""
            }
        }

class PaginationData(BaseModel):
    total_posts: int
    total_pages: int
    current_page: int
    next_url: Optional[str]
    prev_url: Optional[str]
    post_content: List[PostContent]  

class LoginRequest(BaseModel):
    email: str
    password: str

class ErrorResponse(BaseModel):
    detail: str