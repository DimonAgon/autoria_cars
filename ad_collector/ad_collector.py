import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from car_scrapper.scrapper import *
from db.models import *
from db.session_delivery import session_delivery
from static_text import *


@session_delivery.deliver_session
async def collect(search_url: str, session: AsyncSession) -> list[Base]:
    ads: Type[ResultSet] = AutoriaCarScrapper.autoria_ads_scrap(search_url)
    unique = []

    for ad in ads:
        external_id = ad['data-advertisement-id']
        content = AutoriaCarScrapper.autoria_ad_content_scrap(ad)
        clickOn_ad_link = content.find('a', attrs={'class': "address"})
        model_name = clickOn_ad_link.find('span', attrs={'class': "blue bold"}).text.strip()
        source_href = clickOn_ad_link['href']
        pic_href = "https://bidfax.info/" + "/".join(model_name.split())
        price_in_USD = content.find('span', attrs={'class': "bold size22 green"}).text.replace(" ", "")

        in_db_query = select(CarAd).where(CarAd.external_id == external_id)
        in_db = (await session.execute(in_db_query)).scalar()
        if in_db:
            logging.info(in_db_check_True_logging_info_message.format(f"{type(in_db)}{in_db.__repr__()}"))

        else:
            logging.info(in_db_check_False_logging_info_message.format
                         (
                f"external_id={external_id},"
                f" source_href={source_href},"
                f" pic_href={pic_href},"
                f" model_name={model_name},"
                f" price_in_USD={price_in_USD})")
            )
            new_ad = (CarAd
                (
                external_id=external_id,
                model_name=model_name  ,
                source_href=source_href,
                pic_href=pic_href      ,
                price_in_USD=price_in_USD)
            )

            await session.merge(new_ad)
            await session.commit()
            unique.append(new_ad)

    return unique



