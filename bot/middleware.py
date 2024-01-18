
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from db.session_delivery import session_delivery


class DbSessionMiddleware(BaseMiddleware):

    @session_delivery.deliver_session
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
            session: AsyncSession
    ) -> Any:

        data["session"] = session
        return await handler(event, data)