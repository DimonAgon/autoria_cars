
from sqlalchemy.ext.asyncio import async_sessionmaker

from .session_maker import session_maker

from functools import wraps


class SessionDelivery:
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool


    def deliver_session(self, function):

        @wraps(function)
        async def wrap(*args, **kwargs):
            async with self.session_pool() as session:
                return await function(session=session, *args, **kwargs)

        return wrap

session_delivery = SessionDelivery(session_maker)