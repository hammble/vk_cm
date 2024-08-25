import json

from vkbottle.bot import BotLabeler, Bot, Message

from utils.utils import get_user_id, user_id_get_mes, get_user_name

from config import token_bot

bl = BotLabeler()
bl.vbml_ignore_case = True

bot = Bot(token_bot)

def load_muted_users(chat_id):
    try:
        with open(f"{chat_id}.json", 'r') as file:
            muted_users = json.load(file)
    except FileNotFoundError:
        muted_users = []
    return muted_users

def save_muted_users(muted_users, chat_id):
    with open(f"{chat_id}.json", 'w') as file:
        json.dump(muted_users, file)

@bl.chat_message(text = ['/sethelper'])
async def add_helper(message: Message):
    chat_info = await bot.api.messages.get_conversation_members(peer_id=message.peer_id)
    admins = [member for member in chat_info.items if member.is_admin]
    for admin in admins:
        if message.from_id == admin.member_id:

            user_id = await user_id_get_mes(message)

            if user_id < 0:
                await message.reply(
                    "📚 >> Вы можете назначить на роль <<Helper>> только пользователей."
                )
                return

            if user_id == message.from_id:
                await message.reply(
                    "📚 >> Вы можете назначить на роль <<Helper>> любого другого участника, но не себя."
                )
                return

            muted_users = load_muted_users(chat_id = message.chat_id)

            if user_id in muted_users:
                await message.reply(
                    "💡 >> Данный человек уже находится под рангом <<Helper>>."
                )
                
                return
            
            muted_users.append(user_id)
            save_muted_users(muted_users, chat_id = message.chat_id)

            await message.reply(
                "✅ >> Человек назначен на роль <<Helper>>."
            )

@bl.chat_message(text = ['/delhelper'])
async def del_helper(message: Message):
    chat_info = await bot.api.messages.get_conversation_members(peer_id=message.peer_id)
    admins = [member for member in chat_info.items if member.is_admin]
    for admin in admins:
        if message.from_id == admin.member_id:

            user_id = await user_id_get_mes(message)

            if user_id == message.from_id:
                await message.reply(
                    "📚 >> Вы можете снять с роль <<Helper>> любого другого участника, но не себя."
                )
                return

            muted_users = load_muted_users(chat_id = message.chat_id)

            if user_id not in muted_users:
                await message.reply(
                    "💡 >> Данный человек не находится под рангом <<Helper>>."
                )
                
                return
            
            muted_users.remove(user_id)
            save_muted_users(muted_users, chat_id = message.chat_id)

            await message.reply(
                "✅ >> Человек снят с роли <<Helper>>."
            )

@bl.chat_message(text = ['/sethelper <url>'])
async def add_helper(message: Message, url: str):
    chat_info = await bot.api.messages.get_conversation_members(peer_id=message.peer_id)
    admins = [member for member in chat_info.items if member.is_admin]
    for admin in admins:
        if message.from_id == admin.member_id:

            user_id = get_user_id(url)[0]

            if user_id < 0:
                await message.reply(
                    "📚 >> Вы можете назначить на роль <<Helper>> только пользователей."
                )
                return

            if user_id == message.from_id:
                await message.reply(
                    "📚 >> Вы можете назначить на роль <<Helper>> любого другого участника, но не себя."
                )
                return

            muted_users = load_muted_users(chat_id = message.chat_id)

            if user_id in muted_users:
                await message.reply(
                    "💡 >> Данный человек уже находится под рангом <<Helper>>."
                )
                
                return
            
            muted_users.append(user_id)
            save_muted_users(muted_users, chat_id = message.chat_id)

            await message.reply(
                "✅ >> Человек назначен на роль <<Helper>>."
            )

@bl.chat_message(text = ['/delhelper <url>'])
async def del_helper(message: Message, url: str):
    chat_info = await bot.api.messages.get_conversation_members(peer_id=message.peer_id)
    admins = [member for member in chat_info.items if member.is_admin]
    for admin in admins:
        if message.from_id == admin.member_id:

            user_id = get_user_id(url)[0]

            if user_id == message.from_id:
                await message.reply(
                    "📚 >> Вы можете снять с роль <<Helper>> любого другого участника, но не себя."
                )
                return

            muted_users = load_muted_users(chat_id = message.chat_id)

            if user_id not in muted_users:
                await message.reply(
                    "💡 >> Данный человек не находится под рангом <<Helper>>."
                )
                
                return
            
            muted_users.remove(user_id)
            save_muted_users(muted_users, chat_id = message.chat_id)

            await message.reply(
                "✅ >> Человек снят с роли <<Helper>>."
            )

@bl.chat_message(text=['/helpers'])
async def list_helpers(message: Message):
    chat_id = message.chat_id
    chat_info = await bot.api.messages.get_conversation_members(peer_id=message.peer_id)
    admins = [member for member in chat_info.items if member.is_admin]
    if any(message.from_id == admin.member_id for admin in admins):

        muted_users = load_muted_users(chat_id)

        if not muted_users:
            await message.reply("🔍 >> Список хелперов пуст.")
            return
        
        helpers_list = ""
        for user_id in muted_users:
            username = await get_user_name(user_id)
            helpers_list += f"👤 {username}\n"

        await message.reply(f"📝 >> Helpers:\n{helpers_list}")