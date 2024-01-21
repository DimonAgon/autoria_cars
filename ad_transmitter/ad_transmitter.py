
import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ad_collector.ad_collector import AdCollector
from bot.ad_transmitter import bot_transmitter_handlers
from db.session_delivery import session_delivery
from db.models import *
from misc.static_text import *

from typing import Type, List, Iterable


def unique_demands(demands: Iterable[Type[SearchDemand]]):
    unique = []
    unique_values = []
    for demand in demands:
        values = (demand.search_href, demand.target_chat_id)
        if values not in unique_values:
            unique.append(demand)
            unique_values.append(values)

    return unique



async def advertise(demand: Type[SearchDemand]):
    target_chat_id = demand.target_chat_id
    ad_collector = AdCollector(demand)

    while True:
        await asyncio.sleep(1)
        fresh_ads = await ad_collector.collect()

        for ad in fresh_ads:
            await bot_transmitter_handlers.send_chat_ad(ad, target_chat_id)


@session_delivery.deliver_session
async def initial_transmit(session: AsyncSession):
    loop = asyncio.get_running_loop()

    get_all_demands_query = select(SearchDemand)
    demands: List[Type[CarAd]] = (await session.execute(get_all_demands_query)).all()
    for demand in unique_demands(demands):
        loop.create_task(advertise(*demand))
        logging.info(on_search_demand_ad_transmission_initiated_logging_info_message.format(demand.__repr__()))


async def transmit(demand: Type[SearchDemand]):
    loop = asyncio.get_running_loop()
    loop.create_task(advertise(demand))
    logging.info(on_search_demand_ad_transmission_initiated_logging_info_message.format(demand.__repr__()))



