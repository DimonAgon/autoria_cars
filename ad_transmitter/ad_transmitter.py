
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
        unpacked_demand, *_ = demand
        values = (unpacked_demand.search_href, unpacked_demand.target_chat_id)
        if values not in unique_values:
            unique.append(unpacked_demand)
            unique_values.append(values)

    return unique

class Advertiser:

    def __init__(self, demand):
        self.demand = demand
        self.target_chat_id = demand.target_chat_id
        self.ad_collector = AdCollector(demand)
    async def advertise(self):
        target_chat_id = self.target_chat_id
        ad_collector = self.ad_collector

        while True:
            await asyncio.sleep(600)
            fresh_ads = await ad_collector.collect_fresh()
            deleted_ads = await ad_collector.collect_deleted()

            for ad in fresh_ads:
                await bot_transmitter_handlers.send_chat_ad(ad, target_chat_id)

            for ad in deleted_ads:
                await bot_transmitter_handlers.send_chat_ad(ad, target_chat_id, deleted=True)

@session_delivery.deliver_session
async def initial_transmit(session: AsyncSession):
    loop = asyncio.get_running_loop()

    get_all_demands_query = select(SearchDemand)
    demands: List[Type[CarAd]] = (await session.execute(get_all_demands_query)).all()
    for demand in unique_demands(demands):
        advertiser = Advertiser(demand)
        loop.create_task(advertiser.advertise())
        logging.info(on_search_demand_ad_transmission_initiated_logging_info_message.format(demand.__repr__()))


async def transmit(demand: Type[SearchDemand]):
    advertiser = Advertiser(demand)
    loop = asyncio.get_running_loop()
    loop.create_task(advertiser.advertise())
    logging.info(on_search_demand_ad_transmission_initiated_logging_info_message.format(demand.__repr__()))



