from vkbottle.bot import BotLabeler, Message

bl = BotLabeler()
bl.vbml_ignore_case = True

@bl.chat_message(text = ['/ping'])
async def ping(message: Message):
    await message.reply("✅ >> PONG!")