import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import inspect

from car_scrapper.scrapper import *
from db.models import *
from db.session_delivery import session_delivery
from misc.checkers import *
from misc.static_text import *

from typing import Type, List
from bs4 import Tag, ResultSet


class AdCollector:

    def __init__(self, demand: Type[SearchDemand]):
        self.demand = demand
        self.search_url = demand.search_href

    @session_delivery.deliver_session
    async def collect_fresh(self, session: AsyncSession) -> List[Type[CarAd]]:

        ads: Type[ResultSet] = AutoriaCarScrapper.autoria_ads_scrap(self.search_url)
        unique = []

        for ad in ads:
            external_id = ad['data-advertisement-id']
            content = AutoriaCarScrapper.autoria_ad_content_scrap(ad)
            clickOn_ad_link = content.find('a', attrs={'class': "address"})
            model_name = clickOn_ad_link.find('span', attrs={'class': "blue bold"}).text.strip()
            source_href = clickOn_ad_link['href']
            pic_href = "https://bidfax.info/" + "/".join(model_name.split())
            price_in_USD = content.find('span', attrs={'class': "bold size22 green"}).text.replace(" ", "")

            in_db_query = select(CarAd).where(CarAd.external_id == external_id, )
            if not await in_db_checker(in_db_query):
                logging.info(in_db_check_False_logging_info_message.format
                             (
                    f"external_id={external_id},"
                    f" source_href={source_href},"
                    f" pic_href={pic_href},"
                    f" model_name={model_name},"
                    f" price_in_USD={price_in_USD})")
                )

                ad = (CarAd
                    (
                    external_id=external_id  ,
                    model_name=model_name    ,
                    source_href=source_href  ,
                    pic_href=pic_href        ,
                    price_in_USD=price_in_USD,
                    bonded_search_demands=[self.demand])
                )

                await session.merge(ad)
                await session.commit()
                unique.append(ad)

            else:
                ad = (await session.execute(in_db_query)).scalar()

                if not (self.demand.search_href, self.demand.target_chat_id)\
                       in \
                       [(d.search_href, d.target_chat_id) for d in ad.bonded_search_demands]:
                    unique.append(ad)
                    ad.bonded_search_demands.append(self.demand)
                    await session.commit()

        return unique


    @session_delivery.deliver_session
    async def bonded_ads(self, session: AsyncSession):
        result = []

        all_demands_query = select(SearchDemand)
        all_demands = (await session.execute(all_demands_query)).all()
        values = (self.search_url, self.demand.target_chat_id)
        for demand in all_demands:
            demand_unpacked, *_ = demand
            if values == (demand_unpacked.search_href, demand_unpacked.target_chat_id):
                if bonded_cars:=demand_unpacked.bonded_car_ads:
                    result.extend(bonded_cars)

        return result

    def find_tag_sibling_to_car_ad(self, ad: Type[CarAd]) -> Type[Tag]:
        ad_tags: Type[ResultSet] = AutoriaCarScrapper.autoria_ads_scrap(self.search_url)

        for tag in ad_tags:
            if ad.external_id == int(tag['data-advertisement-id']):
                return tag

    async def collect_deleted(self) -> List[Type[CarAd]]:
        deleted = []

        for ad in await self.bonded_ads():
            is_depleted = None
            if self.find_tag_sibling_to_car_ad(ad):
                is_depleted = False

            if is_depleted:
                deleted.append(ad)

        return deleted


    @session_delivery.deliver_session
    async def collect_repriсed(self, session: AsyncSession) -> List[Type[CarAd]]:
        repriced = []

        ad_tags: Type[ResultSet] = AutoriaCarScrapper.autoria_ads_scrap(self.search_url)

        for ad in await self.bonded_ads():
            tag_ad = self.find_tag_sibling_to_car_ad(ad)
            current_price = int(tag_ad.find('span', attrs={'class': "bold size22 green"}).text.replace(" ", ""))
            if not ad.price_in_USD == current_price:
                repriced.append(ad)
                ad.price_in_USD = current_price
                await session.commit()

        return repriced




