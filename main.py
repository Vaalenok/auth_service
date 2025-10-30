import logging
import uvicorn
from colorlog import ColoredFormatter
from contextlib import asynccontextmanager
from fastapi import FastAPI
from core import crud
from core.routes import auth, admin, user
from db.database import engine, Base
from db.models import Roles
from db.initialization import add_start_data

handler = logging.StreamHandler()
formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red"
    }
)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        roles = await crud.get_all(Roles)

        if not roles:
            await add_start_data()

    yield

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def clear_cookie_on_unauthorized(request, call_next):
    response = await call_next(request)
    if response.status_code == 401:
        response.delete_cookie("access_token")
    return response

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=False)
