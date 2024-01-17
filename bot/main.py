
import asyncio

from .bot import bot
from .dispatcher import dispatcher
from .middleware import *

from db.session_maker import session_maker


def set_all_middleware():
    dispatcher.update.middleware(DbSessionMiddleware(session_pool=session_maker))

async def deploy_bot():
    await dispatcher.start_polling(bot)
    await dispatcher.stop
    await bot.session.close()

def main():

    set_all_middleware()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(deploy_bot())
    loop.run_forever()

if __name__ == '__main__':
    main()