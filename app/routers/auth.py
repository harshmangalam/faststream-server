from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm


from ..models import User, UserCreate, UserRead
from ..utils import generate_password_hash, verify_password, create_jwt_token
from ..settings import ACCESS_TOKEN_EXPIRE_MINUTES
from .. dependencies import get_current_user, get_session

router = APIRouter(prefix="/auth", tags=["auth"])



@router.post("/signup", response_model=UserRead)
def signup(user: UserCreate, session: Session = Depends(get_session)):

    # fetch db user by email
    db_user = session.exec(select(User).where(
        User.email == user.email)).first()
    if db_user is not None:
        raise HTTPException(
            status_code=400, detail="Email already exists!")
    # hash plain text password
    user.password = generate_password_hash(user.password)
    # create new user from User instance
    new_user = User.from_orm(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    # fetch db user by email
    db_user = session.exec(select(User).where(
        User.email == form_data.username)).first()
    if db_user is None:
        raise HTTPException(
            status_code=400, detail="Email does not exists!")
    # match user  password
    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password!")
    # create token expiration  in minutes
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # create jwt token
    access_token = create_jwt_token(
        {"sub": str(db_user.id)}, expires_delta=access_token_expires)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }


@router.get("/me", response_model=UserRead,)
def get_current_user(current_user_id: str = Depends(get_current_user), session: Session = Depends(get_session)):
    user = session.get(User, current_user_id)
    return user
