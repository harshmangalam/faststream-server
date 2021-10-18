from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError

from passlib.context import CryptContext
from jose import jwt

from .settings import ALGORITHM, SECRET_KEY

# use bcrypt algorithm to hash password 
passsword_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# hash plain text password 
def generate_password_hash(plain_password):
    return passsword_context.hash(plain_password)

# match plain text password with hash password 
def verify_password(plain_password, hash_password):
    return passsword_context.verify(plain_password, hash_password)

# create new jwt token from user_id 
def create_jwt_token(payload: dict, expires_delta: Optional[timedelta] = None):
    encoded_payload = payload.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    encoded_payload.update({"exp": expire})
    encoded_jwt = jwt.encode(encoded_payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# decode jwt token 
def decode_jwt_token(token):
    return jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)

      
    