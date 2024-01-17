
from aiogram import Router, Dispatcher

dispatcher = Dispatcher()
demands_router = Router()
dispatcher.include_router(demands_router)

