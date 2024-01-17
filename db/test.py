
from asyncio import run as async_run

from sqlalchemy.ext.asyncio import async_sessionmaker

from engine import engine
from models import *

session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def test():
    session = session_maker()
    await session.merge(CarAd(external_id=000, source_href="source_href", pic_href="pic_href", model_name="test_car", price_in_USD="0"))
    await session.commit()

if __name__ == "__main__":
    async_run(test())



