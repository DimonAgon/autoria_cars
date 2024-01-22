
from ..bot import bot
from db.models import CarAd

from typing import Type


def transform_to_chat_ad(ad: Type[CarAd], deleted: bool=False) -> str:
    chat_ad = f"{ad.model_name}\n{ad.price_in_USD}\n{ad.source_href}\n{ad.pic_href}"
    if not deleted:
        return chat_ad

    else:
        return "\u0336".join(chat_ad) + "\u0336"


async def send_chat_ad(ad: Type[CarAd], chat_id: int, deleted: bool=False) -> None:
    chat_ad = transform_to_chat_ad(ad, deleted)
    await bot.send_message(chat_id, chat_ad)

