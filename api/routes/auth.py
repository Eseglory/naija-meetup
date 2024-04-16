from fastapi import APIRouter, Depends, status, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from ..utilities import utils
from ..oauth2 import create_access_token
from ..schemas import LoginRequest

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

# @router.post("", status_code=status.HTTP_200_OK)
# async def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
#     user = await utils.db["users"].find_one({"username": user_credentials.username})
#     if user["is_email_verified"] == False:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have not completed your registration process")

#     if user and utils.verify_password(user_credentials.password, user["password"]):
#         access_token = create_access_token({"id": user["_id"]})
#         return ({"access_token": access_token, "token_type": "bearer"})
#     else:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user credentials")

@router.post("", status_code=status.HTTP_200_OK)
async def login(user_credentials: LoginRequest):

    if not user_credentials.username or not user_credentials.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username and password are required")

    user = await utils.db["users"].find_one({"username": user_credentials.username})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    if user["is_email_verified"] == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have not completed your registration process")

    if user and utils.verify_password(user_credentials.password, user["password"]):
        access_token = create_access_token({"id": user["_id"]})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user credentials")