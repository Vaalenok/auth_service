from security import config
import logging
import uuid
from functools import wraps
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(
    f"postgresql+asyncpg://{config.DB_USERNAME}:{config.DB_PASSWORD}@{config.DB_IP}:{config.DB_PORT}/{config.DB_NAME}",
    echo=False,
    pool_pre_ping=True
)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    def __repr__(self):
        return f"<{self.__class__.__name__} (id={self.id})>"

def connection(commit: bool = True):
    def decorator(method):
        @wraps(method)
        async def wrapper(*args, **kwargs):
            async with async_session_maker() as session:
                try:
                    kwargs["session"] = session
                    result = await method(*args, **kwargs)

                    if commit:
                        await session.commit()

                    return result
                except Exception as e:
                    logging.error(e)
                    await session.rollback()
                finally:
                    await session.close()
        return wrapper
    return decorator
