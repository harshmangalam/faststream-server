from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Optional


from ..dependencies import get_current_user, get_session
from ..models import User, UserRead, UserReadWithVideos, UserUpdate

router = APIRouter(tags=["users"], prefix="/users")


@router.get("/", response_model=List[UserRead])
def get_users(limit: Optional[int] = None, offset: Optional[int] = None, session: Session = Depends(get_session)):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.get("/{user_id}", response_model=UserReadWithVideos)
def get_user_by_id(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found!")

    return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_data: UserUpdate, session: Session = Depends(get_session), current_user_id: int = Depends(get_current_user)):

    if current_user_id != user_id:
        raise HTTPException(
            status_code=403, detail="Unauthorized access denied!")

    db_user = session.get(User, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found!")

    user_dict = user_data.dict(exclude_unset=True)

    for key, value in user_dict.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session), current_user_id: int = Depends(get_current_user)):
    if current_user_id != user_id:
        raise HTTPException(
            status_code=403, detail="Unauthorized access denied!")

    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")
    session.delete(db_user)
    session.commit()
    return {"deleted": True}
