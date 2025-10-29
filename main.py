import logging
import uvicorn
from colorlog import ColoredFormatter
from contextlib import asynccontextmanager
from fastapi import FastAPI
from core import crud
from core.routes import auth
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
app.include_router(auth.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=False)
