from vkbottle.bot import BotLabeler, Bot, Message
from vkbottle import VKAPIError

from routes.disallow_words import load_data
from routes.helpers import load_muted_users

from config import token_bot

bot = Bot(token_bot)

bl = BotLabeler()
bl.vbml_ignore_case = True

@bl.chat_message()
async def logmes(message: Message):
    chat_info = await bot.api.messages.get_conversation_members(peer_id=message.peer_id)
    admins = [member for member in chat_info.items if member.is_admin]
    for admin in admins:
        if message.from_id != admin.member_id:
            chat_id = message.chat_id
            blocked_words = load_data(chat_id)
            muted_users = load_muted_users(chat_id)
            for word in blocked_words:
                if word.lower() in message.text.lower():
                    try:

                        if message.from_id > 0:

                            if message.from_id in muted_users:
                                return

                            await bot.api.messages.delete(
                                peer_id = message.peer_id,
                                delete_for_all = True,
                                cmids = [message.conversation_message_id]
                            )

                            await bot.api.messages.remove_chat_user(
                                chat_id = chat_id,
                                user_id = message.from_id
                            )

                            await message.answer(
                                f"⚠ Пользователь @id{message.from_id} был исключён с чата.\n"
                                "⚙ >> Сообщение пользователя содержало запрещённое слово.\n\n"
                                "📚 >> Список запрещённых слов <</bwords>>\n"
                                "💡 >> Если желаете разрешить конкретному человеку отправлять запрещённые слова, выдайте человеку ранг <<Helper>>.\n"
                                "⚙ >> Команда <</sethelper (ссылка / ответ на сообщение)"
                            )

                    except VKAPIError:
                        pass