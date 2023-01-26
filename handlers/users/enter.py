from aiogram import types

from loader import dp
from utils.db_api import quick_commands as commands


@dp.message_handler(commands='enter')
async def enter_command(message: types.Message):
    try:
        await commands.update_user_status(message.from_user.id, True)
        await message.answer('You entered to chat')
    except Exception:
        await message.answer('Press /start to register')
        print('Status update error')
