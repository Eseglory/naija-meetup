from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..utilities import utils, send_email
from ..oauth2 import create_access_token
from ..schemas import PasswordReset, CompletePasswordReset

router = APIRouter(
    prefix="/password-reset",
    tags=["Authentication"]
)

@router.post("", response_description="Reset password")
async def reset_password(user_email: PasswordReset):
    user = await utils.db["users"].find_one({"email": user_email.email})
    if user is not None:
        otp = await utils.generate_and_insert_otp(user["email"])
        message = f"Your One-Time Password (OPT) to reset your Naija-meet app. password is: <strong>{otp}</strong>"
        await send_email.send_custom_email("Naija-meetup reset password", user["email"], otp, user["first_name"], message)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user with this email address not found."
        )
    return ({"message": "operation was successful."})

@router.put("/complete", response_description="Complete password reset")
async def complete_reset_password(user_request: CompletePasswordReset):
    is_otp_expired = await utils.is_otp_expired(user_request.otp, user_request.email)
    if is_otp_expired:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="You have entered an invalid otp, kindly request for new otp or reset password again.")
    update_otp = await utils.update_otp_usage(user_request.otp)
    if update_otp == False:
        raise HTTPException(
            status_code=404, detail="unable to process otp.")
    
    get_user = await utils.db["users"].find_one({"email": user_request.email})
    get_user["password"] = utils.get_password_hash(user_request.new_password)

    update_user = await utils.db["users"].update_one({"_id": get_user["_id"]},
                                                     {"$set": get_user})
    if update_user.modified_count == 1:
        return ({"message": "Operation successful."})
    raise HTTPException(
        status_code=404, detail="User information not found."
    )

