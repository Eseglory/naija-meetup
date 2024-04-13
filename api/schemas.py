from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid ObjectID")
#         return ObjectId(v)

#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(type="string")

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
    username: str
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
                "username": "sammy",
                "first_name": "Samson",
                "last_name": "John",
                "email": "sammy@gmail.com",
                "password": "zA@322445&^"
            }
        }

class UserResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    username: str
    first_name: str
    last_name: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "sammy",
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
    title: str
    content: str
    featured_image: str
    is_published: bool = True
    creation_date: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "It's a brigth day",
                "content": "enter more details here",
                "featured_image": "",
                "is_published": True
            }
        }

class PostContentResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_email: str = None
    post_owner: str =None
    title: str
    content: str
    featured_image: str
    is_published: bool = True
    creation_date: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "It's a brigth day",
                "content": "enter more details here",
                "featured_image": "",
                "is_published": True
            }
        }


