import motor.motor_asyncio
from passlib.context import CryptContext
from datetime import datetime, timedelta
import random
import string
from dotenv import load_dotenv
import os

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db = client.naija_meetup

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def generate_otp():
    otp = ''.join(random.choices(string.digits, k=6))
    return otp

def generate_expiry_time():
    return datetime.now() + timedelta(minutes=10)

async def generate_and_insert_otp(user_email):
    otp = generate_otp()
    expiry_time = generate_expiry_time()
    otp_data = {
        "user_email": user_email,
        "otp_code": otp,
        "created_at": datetime.now(),
        "is_used": False,
        "used_at": None
    }
    result = await db["otp_verifications"].insert_one(otp_data)
    return str(otp)

async def is_otp_expired(otp: str, user_email: str):
    otp_data = await db["otp_verifications"].find_one({"otp_code": otp, "user_email": user_email})
    if otp_data is None:
        return True
    elif otp_data["is_used"]:
        return True
    else: 
        current_time = datetime.now()
        expiry_time = otp_data["created_at"] + timedelta(minutes=10)
        if current_time > expiry_time:
            return True  # OTP has expired
        else:
            return False  # OTP is still valid
        
async def update_otp_usage(otp: str):
        current_otp = await db["otp_verifications"].find_one({"otp_code": otp})
        current_otp["is_used"] = True
        update_otp = await db["otp_verifications"].update_one({"_id": current_otp["_id"]},
                                                        {"$set": current_otp})
        if update_otp.modified_count == 1:
            return True
        else:
            return False
