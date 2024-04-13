from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from ..schemas import User, UserResponse, CompleteUserRegistration
import secrets
from ..utilities import utils, send_email

router = APIRouter(tags=["User Routes"])


@router.post("/user-registration", response_description="Register a new user", response_model=UserResponse)
async def registration(user_info: User):
    user_info = jsonable_encoder(user_info)

    username_found = await utils.db["users"].find_one({"username": user_info["username"]})
    email_found = await utils.db["users"].find_one({"email": user_info["email"]})
    if username_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"username {user_info["username"]} already taken.")

    if email_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"email {user_info["email"]} already exist.")

    user_info["password"] = utils.get_password_hash(user_info["password"])
    user_info["apikey"] = secrets.token_hex(30)
    new_user = await utils.db["users"].insert_one(user_info)
    created_user = await utils.db["users"].find_one({"_id": new_user.inserted_id})

    otp = await utils.generate_and_insert_otp(user_info["email"])
    await send_email.send_otp_email(user_info["email"], otp, user_info["first_name"])
    return created_user

@router.post("/verify-user", response_description="Resend otp")
async def registration(user_request: CompleteUserRegistration):
    is_otp_expired = await utils.is_otp_expired(user_request.otp, user_request.email)
    if is_otp_expired:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="You have entered an invalid otp, kindly request for new otp.")
    update_otp = await utils.update_otp_usage(user_request.otp)
    if update_otp == False:
        raise HTTPException(
            status_code=404, detail="unable to process otp.")
    
    get_user = await utils.db["users"].find_one({"email": user_request.email})
    get_user["is_email_verified"] = True

    update_user = await utils.db["users"].update_one({"_id": get_user["_id"]},
                                                     {"$set": get_user})
    if update_user.modified_count == 1:
        return ({"message": "Operation successful."})
    raise HTTPException(
        status_code=404, detail="User information not found."
    )

    return ({"message": f"User verification was successful"})

@router.post("/resend-otp", response_description="Resend otp")
async def registration(user_email: str):
    otp = await utils.generate_and_insert_otp(user_email)
    await send_email.send_otp_email(user_email, otp, "There")
    return ({"message": f"Operation successful, a new otp has been sent to {user_email}"})


