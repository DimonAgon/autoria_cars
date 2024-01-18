
import asyncio

from __init__ import *
from db.main import main as db_main
from bot.main import deploy_bot
from ad_transmitter import ad_transmitter

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(db_main())
    loop.create_task(ad_transmitter.initial_transmit())
    loop.create_task(deploy_bot())
    loop.run_forever()

if __name__ == "__main__":
    main()