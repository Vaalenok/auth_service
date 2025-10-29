import asyncio
from db.database import engine, Base
from db.initialization import add_start_data

async def reset_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await add_start_data()

if __name__ == "__main__":
    asyncio.run(reset_db())
