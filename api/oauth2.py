from fastapi import HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import os
from typing import Dict
from .schemas import TokenData
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from .utilities import utils

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(payload: Dict):
    to_encode = payload.copy()
    expiration_time = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiration_time})

    jwt_token = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("id")
        if not id:
            raise credential_exception
        token_data = TokenData(id=id)
        return token_data
    except JWTError:
        raise credential_exception
    
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credential_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Token could not be verified.",
#         headers={"WWW-AUTHENTICATE": "Bearer"}
#     )
#     current_user_id = verify_access_token(token, credential_exception).id
#     current_user = await utils.db["users"].find_one({"_d": current_user_id})

#     return current_user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token could not be verified.",
        headers={"WWW-AUTHENTICATE": "Bearer"}
    )
    try:
        token_data = verify_access_token(token, credential_exception)
        if token_data is None:
            raise credential_exception
        current_user = await utils.db["users"].find_one({"_id": token_data.id})

        if current_user is None:
            raise credential_exception
        return current_user

    except Exception as e:
        raise credential_exception from e

