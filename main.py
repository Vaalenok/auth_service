import asyncio
import asyncpg
import logging
from colorlog import ColoredFormatter
from flask import Flask
import config
import crud
from database import engine, Base
from models import Roles
from initialization import add_start_data

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

async def init_db():
    retries = 5

    while retries > 0:
        try:
            async with engine.begin() as conn:
                # await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

                roles = await crud.get_all(Roles)

                if not roles:
                    await add_start_data()

                return
        except asyncpg.exceptions.CannotConnectNowError as e:
            retries -= 1
            logging.error(f"{e}\n\nОсталось попыток: {retries}")
            await asyncio.sleep(5)

def create_app():
    app = Flask("auth_service")
    app.config["SECRET_KEY"] = config.FLASK_KEY

    # from routes import bp
    # app.register_blueprint(bp)

    app.run(debug=True, use_reloader=False)

async def main():
    await init_db()
    create_app()

if __name__ == "__main__":
    asyncio.run(main())
