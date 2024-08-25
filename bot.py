from vkbottle import Bot
from routes import labelers

from config import token_bot

bot = Bot(token_bot)

for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)

bot.run_forever()