
from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from db.session_delivery import session_delivery
from db.models import *
from misc.static_text import *

from typing import Type

import logging


@session_delivery.deliver_session
async def in_db_checker(in_db_query: Type[Select], session: AsyncSession) -> bool:

    in_db = (await session.execute(in_db_query)).scalar_one_or_none()

    if in_db:
        logging.info(in_db_check_True_logging_info_message.format(f"{type(in_db)}{in_db.__repr__()}"))
        return True

    else:
        logging.info(in_db_check_False_logging_info_message.format(f"{type(in_db)}{in_db.__repr__()}"))
        return False