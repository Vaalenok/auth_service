import asyncio
import asyncpg
import logging
from colorlog import ColoredFormatter
from database import engine, Base

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
    retries = 10

    while retries > 0:
        try:
            async with engine.begin() as conn:
                # await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)
                return
        except asyncpg.exceptions.CannotConnectNowError as e:
            retries -= 1
            logging.error(f"{e}\n\nОсталось попыток: {retries}")
            await asyncio.sleep(5)

async def main():
    tasks = [
        init_db()
    ]

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        logging.info("Сервис запущен")
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Сервис остановлен")
