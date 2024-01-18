
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import types

from .bot import bot
from .dispatcher import dispatcher, demands_router
from .validators import *
from .filters import *
from db.models import *
from static_text import *

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import logging


class SearchDemandStates(StatesGroup):
    demand = State()

@dispatcher.message(Command(commands=['search_demand', 'demand']))
async def search_demand_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    chat_id = message.chat.id
    await state.set_state(SearchDemandStates.demand)
    await message.answer(search_demand_url_request_chat_message, 'Markdown')
    logging.info(on_search_demand_url_request_logging_info_message.format(user_id, chat_id))

@dispatcher.message(NoCommandFilter(), SearchDemandStates.demand)
async def search_demand(message: types.Message, state: FSMContext, session: AsyncSession):
    user_id = message.from_user.id
    chat_id = message.chat.id
    message_text = message.text
    logging.info(search_demand_submission_initiated_logging_info_message.format(message_text, user_id, chat_id))
    await message.answer(search_demand_submission_initiated_chat_message)

    try:
        if validate_autoria_search_url_is_authentic(message_text):
            await message.answer(autoria_search_url_authenticity_validation_success_chat_message)

        else:
            await message.answer(autoria_search_url_authenticity_validation_failure_chat_message)
            return

        if validate_autoria_search_url_points_on_real_source(message_text):
            await message.answer(autoria_search_url_points_on_real_source_validation_success_chat_message)

        else:
            await message.answer(autoria_search_url_points_on_real_source_validation_failure_chat_message.format(
                message_text, user_id, chat_id))
            return

        demand_attrs = {'search_href': message_text, 'target_chat_id': chat_id}
        in_db_query = select(SearchDemand).where(SearchDemand.search_href == demand_attrs['search_href'],
                                   SearchDemand.target_chat_id == demand_attrs['target_chat_id'])
        in_db = (await session.execute(in_db_query)).scalar()
        if not in_db:
            logging.info(in_db_check_False_logging_info_message.format(in_db.__repr__))
            await message.answer(not_in_db_validation_success_chat_message)

        else:
            logging.info(in_db_check_True_logging_info_message.format(in_db.__repr__))
            await message.answer(not_in_db_validation_failure_chat_message)
            return

        await session.merge(SearchDemand(**demand_attrs))
        await session.commit()
        logging.info(search_demand_on_submission_success_logging_info_message.format(message_text, user_id, chat_id))
        await message.answer(search_demand_submission_success_chat_message)

    except Exception as e:
        logging.error(e)
        logging.error(search_demand_on_submission_failure_logging_error_message.format(message_text, user_id, chat_id))
        await message.answer(search_demand_submission_failure_chat_message)

    await state.clear()







