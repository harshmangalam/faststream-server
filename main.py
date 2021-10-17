from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.routers import auth as auth_router
from app.routers import videos as videos_router

from app.settings import PORT, HOST

from app.database import create_db_and_tables

app = FastAPI(version="1.0.0",title="FastStream")

app.mount("/static",StaticFiles(directory="static"),name="static")

app.include_router(auth_router.router)
app.include_router(videos_router.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def health_check():
    return {"msg": "server up and running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT,
                log_level="info", reload=True)