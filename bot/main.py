
import asyncio

from .bot import bot
from .dispatcher import dispatcher
from .middleware import *


def set_all_middleware():
    dispatcher.update.middleware(DbSessionMiddleware())

async def deploy_bot():
    set_all_middleware()
    await dispatcher.start_polling(bot)
    await dispatcher.stop
    await bot.session.close()

def main():

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(deploy_bot())
    loop.run_forever()

if __name__ == '__main__':
    main()