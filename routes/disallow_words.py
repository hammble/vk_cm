import json

from vkbottle.bot import BotLabeler, Bot, Message
from config import token_bot

bot = Bot(token_bot)

bl = BotLabeler()
bl.vbml_ignore_case = True

blocked_words_dict = {}

def load_data(chat_id):
    try:
        with open(f"blocked_words_{chat_id}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return[]

def save_data(chat_id, blocked_words):
    with open(f"blocked_words_{chat_id}.json", "w") as file:
        json.dump(blocked_words, file)

@bl.chat_message(text = ['/bword <word>'])
async def banword(message: Message, word: str):
    chat_info = await bot.api.messages.get_conversation_members(peer_id=message.peer_id)
    admins = [member for member in chat_info.items if member.is_admin]
    for admin in admins:
        if message.from_id == admin.member_id:
            chat_id = message.chat_id
            global blocked_words_dict
            if chat_id not in blocked_words_dict:
                blocked_words_dict[chat_id] = load_data(chat_id)
            word_lower = word.lower()
            if word_lower not in blocked_words_dict[chat_id]:
                blocked_words_dict[chat_id].append(word_lower)
                save_data(chat_id, blocked_words_dict[chat_id])
                await message.reply("✅ >> Добавил слово в список запрещённых слов.")
            else:
                await message.reply("🔹 >> Слово уже было запрещено. Список: <</bwords>>")

@bl.chat_message(text = ['/uword <word>'])
async def banword(message: Message, word: str):
    chat_info = await bot.api.messages.get_conversation_members(peer_id=message.peer_id)
    admins = [member for member in chat_info.items if member.is_admin]
    for admin in admins:
        if message.from_id == admin.member_id:
            chat_id = message.chat_id
            blocked_words = load_data(chat_id)
            word_lower = word.lower()
            if word_lower in blocked_words:
                blocked_words.remove(word_lower)
                save_data(chat_id, blocked_words)
                await message.reply("✅ >> Удалил слово из списка запрещённых слов.")
            else:
                await message.reply("🔹 >> Слово не было запрещено. Список: <</bwords>>")

@bl.message(text=['/bwords'])
async def trh(message: Message):
    chat_info = await bot.api.messages.get_conversation_members(peer_id=message.peer_id)
    admins = [member for member in chat_info.items if member.is_admin]
    for admin in admins:
        if message.from_id == admin.member_id:
            chat_id = message.chat_id
            blocked_words = load_data(chat_id)
            if not blocked_words:
                await message.reply("🔹 >> Список запрещенных слов пуст.")
            else:
                blocked_words_str = "\n".join(blocked_words)
                await message.reply(f"{blocked_words_str}")