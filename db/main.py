
import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker
from models import Base

from engine import engine

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

if __name__ == "__main__":
    asyncio.run(main())