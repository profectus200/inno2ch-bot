from datetime import datetime, timedelta

from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.models.message import Message
from utils.db_api.models.user import User


async def add_user(user_id: int):
    try:
        user = User(user_id=user_id, status=False)
        await user.create()
    except UniqueViolationError:
        print('User creation error')


async def get_user_status(user_id):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user.status


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_all_active_users(user_id):
    users = await User.query.where(User.status == True).where(User.user_id != user_id).gino.all()
    return users


async def select_user(user_id):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def update_user_status(user_id, status):
    user = await select_user(user_id)
    await user.update(status=status).apply()


async def delete_user(user_id):
    user = await select_user(user_id)
    await user.delete()


async def add_message(user_id: int, original_id: int, message_id: int):
    try:
        message = Message(user_id=user_id, original_id=original_id, message_id=message_id)
        await message.create()
    except UniqueViolationError:
        print('Message creation error')


async def get_original_message(user_id, message_id):
    message = await Message.query.where(Message.user_id == user_id).where(
        Message.message_id == message_id).gino.first()
    return message.original_id


async def get_replied_message(user_id, original_id):
    message = await Message.query.where(Message.user_id == user_id).where(
        Message.original_id == original_id).gino.first()
    return message.message_id


async def refresh_messages():
    messages = await Message.query.where(Message.created_at < (datetime.now() - timedelta(days=1))).gino.all()
    for message in messages:
        await message.delete()

    while await db.func.count(Message.id).gino.scalar() > 10000:
        message = await Message.query.gino.first()
        await message.delete()
