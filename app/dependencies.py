from fastapi import Depends,HTTPException,status
from jose import JWTError
from sqlmodel import Session
from fastapi.security import OAuth2PasswordBearer

from .database import engine
from .utils import decode_jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")



def get_session():
    with Session(engine) as session:
        yield session


def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_jwt_token(token)

        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    

    return int(user_id)
    