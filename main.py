
from asyncio import run as async_run

from __init__ import *
from db.main import main as db_main
from bot.main import main as bot_main

def main():
    async_run(db_main())
    bot_main()

if __name__ == "__main__":
    main()