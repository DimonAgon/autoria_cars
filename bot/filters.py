import logging

from aiogram.filters import BaseFilter
from aiogram import types

from bot import bot
from static_text import *


class IsAdminFilter(BaseFilter):
    key = 'is_admin'
    required_auth_level = 'administrator'
    creator = 'creator'

    async def __call__(self, message: types.Message) -> bool:

        chat_id = message.chat.id
        user_id = message.from_user.id
        member = await bot.get_chat_member(chat_id, user_id)
        is_admin = member.status == self.required_auth_level or member.status == self.creator

        if is_admin:
            logging.info(is_admin_authorization_success_logging_info_message.format(user_id))
            return True

        else:
            logging.error(is_admin_authorization_failure_logging_info_message.format(user_id))
            await message.answer(is_admin_authorization_failure_chat_message)
            return False
