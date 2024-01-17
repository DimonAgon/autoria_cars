
from sqlalchemy.ext.asyncio import async_sessionmaker

from .engine import engine


session_maker = async_sessionmaker(engine, expire_on_commit=False)
