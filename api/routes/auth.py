from fastapi import APIRouter, Depends, status, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from ..utilities import utils, send_email
from ..oauth2 import create_access_token
from ..schemas import LoginRequest

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

# @router.post("", status_code=status.HTTP_200_OK)
# async def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
#     user = await utils.db["users"].find_one({"email": user_credentials.username})
#     if user["is_email_verified"] == False:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have not completed your registration process")

#     if user and utils.verify_password(user_credentials.password, user["password"]):
#         access_token = create_access_token({"id": user["_id"]})
#         return ({"access_token": access_token, "token_type": "bearer"})
#     else:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user credentials")

@router.post("", status_code=status.HTTP_200_OK)
async def login(user_credentials: LoginRequest):

    if not user_credentials.email or not user_credentials.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email and password are required")

    user = await utils.db["users"].find_one({"email": user_credentials.email, "is_active": True})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user["is_email_verified"] == False:
        otp = await utils.generate_and_insert_otp(user["email"])
        await send_email.send_otp_email(user["email"], otp, user["first_name"])
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have not completed your registration process")

    if user and utils.verify_password(user_credentials.password, user["password"]):
        user_id_str = str(user["_id"])  # Convert ObjectId to string
        access_token = create_access_token({"id": user_id_str})
        return {
            "access_token": access_token,
              "token_type": "bearer",
              "user_details": {
                  "email": user["email"],
                  "first_name": user["first_name"],
                  "last_name": user["last_name"],
                  "registration_date": user["creation_date"] 
              }
                }
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user credentials")