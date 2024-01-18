
from ..bot import bot
from db.models import CarAd

from typing import Type


def transform_to_chat_ad(ad: Type[CarAd]) -> str:
    chat_ad = f"{ad.model_name}\n{ad.price_in_USD}\n{ad.source_href}\n{ad.pic_href}"
    return chat_ad

async def send_chat_ad(ad: Type[CarAd], chat_id: int) -> None:
    chat_ad = transform_to_chat_ad(ad)
    await bot.send_message(chat_id, chat_ad)

