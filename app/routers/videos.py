from fastapi.responses import FileResponse
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Query
from sqlmodel import Session, select
from typing import List, Optional
import shutil
import uuid
import os

from ..models import Video, VideoRead, User, VideoReadWithUser
from ..dependencies import get_current_user, get_session

router = APIRouter(tags=["videos"], prefix="/videos")


@router.post("/", response_model=VideoRead)
def create_video(title: str = Form(...), description: str = Form(...), video_file: UploadFile = File(...), curret_user_id: int = Depends(get_current_user), session: Session = Depends(get_session)):

    user = session.get(User, curret_user_id)
    if user is None:
        raise HTTPException(status_code=400, detail="User account not found!")

    filename = uuid.uuid4()
    extname = os.path.splitext(video_file.filename)[1]

    video_file_name = f"{filename}{extname}"

    with open(f"static/{video_file_name}", "wb+") as buffer:
        shutil.copyfileobj(video_file.file, buffer)

    new_video = Video(title=title, description=description,
                      file_name=video_file_name, content_type=video_file.content_type, user=user)
    session.add(new_video)
    session.commit()
    session.refresh(new_video)
    return new_video


@router.get("/", response_model=List[VideoRead])
def get_videos(limit: Optional[int] = None, offset: Optional[int] = None, session: Session = Depends(get_session)):
    videos = session.exec(select(Video).offset(offset).limit(limit)).all()
    return videos


@router.get("/{video_id}", response_model=VideoReadWithUser)
def get_video_by_id(video_id: int, session: Session = Depends(get_session)):
    video = session.get(Video, video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found!")
    return video


@router.get("/{video_id}/stream")
def stream_video(video_id: int, session: Session = Depends(get_session)):
    video = session.get(Video, video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found!")
    
    video.views += 1
    session.add(video)
    session.commit()
    session.refresh(video)
    return FileResponse(f"static/{video.file_name}")
    


@router.patch("/{video_id}")
def update_video(video_id: int, title: str = Form(None), description: str = Form(None), video_file: UploadFile = File(None), curret_user_id: int = Depends(get_current_user), session: Session = Depends(get_session)):
    user = session.get(User, curret_user_id)
    if user is None:
        raise HTTPException(status_code=400, detail="User account not found!")

    video = session.get(Video, video_id)

    if video is None:
        raise HTTPException(status_code=404, detail="Video not found!")

    if title is not None:
        video.title = title
    if description is not None:
        video.description = description

    if video_file is not None:
        filename = uuid.uuid4()
        extname = os.path.splitext(video_file.filename)[1]

        video_file_name = f"{filename}{extname}"

        with open(f"static/{video_file_name}", "wb+") as buffer:
            shutil.copyfileobj(video_file.file, buffer)

        os.remove(f"static/{video.file_name}")

        video.file_name = video_file_name

    session.add(video)
    session.commit()
    session.refresh(video)

    return video


@router.delete("/{video_id}")
def delete_video(video_id: int, curret_user_id: int = Depends(get_current_user), session: Session = Depends(get_session)):

    user = session.get(User, curret_user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="Account not found!")

    video = session.get(Video, video_id)

    if video is None:
        raise HTTPException(status_code=404, detail="Video not found!")

    os.remove(f"static/{video.file_name}")

    session.delete(video)
    session.commit()

    return {"deleted": True}




@router.post("/{video_id}/toggle_likes",response_model=VideoRead)
def toggle_video_likes(video_id:int, curret_user_id: int = Depends(get_current_user), session: Session = Depends(get_session)):
    user = session.get(User, curret_user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="Account not found!")

    video = session.get(Video, video_id)

    if video is None:
        raise HTTPException(status_code=404, detail="Video not found!")

    
    if user in video.user_likes:
        video.user_likes.remove(user)
    else:
        video.user_likes.append(user)

    session.add(video)
    session.commit()
    session.refresh(video)

    return video
