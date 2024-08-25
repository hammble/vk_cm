from vkbottle.bot import BotLabeler, Message, MessageEvent, rules
from vkbottle.dispatch.rules.base import ChatActionRule
from vkbottle_types.objects import MessagesMessageActionStatus
from vkbottle import Keyboard, KeyboardButtonColor, GroupEventType, Callback

from config import gp_id, link_faq

bl = BotLabeler()

@bl.message(ChatActionRule(MessagesMessageActionStatus.CHAT_INVITE_USER.value))
async def invitebot(message: Message) -> None:
    if (
        message.action is not None
        and message.group_id is not None
        and message.action.member_id == -gp_id
    ):
        
        keyboard = (
            Keyboard(
                one_time = False,
                inline = True
            )
            .add(Callback("📚 F.A.Q", payload = {
                "cmd": "invitebot"
            }), color = KeyboardButtonColor.POSITIVE)
        )

        text = (
            "✨ Доброго времени суток!\n"
            "📌 Я бот, который с радостью поможет вам избавиться от назойливой рекламы в чате.\n"
            "⚒ Прежде чем начать работу со мной, советую ознакомиться с <<F.A.Q>>.\n\n"
            "⚙ >> Список настроек <</settings>>\n"
            "💡 >> При приобретении VIP услуги, возможностей станет больше!\n"
            "💡 >> Обязательно выдайте мне звёздочку (администратора) в чате для корректной работы."
        )

        await message.answer(text, keyboard = keyboard)

@bl.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({"cmd": "invitebot"}),
)
async def keybd(event: MessageEvent):
    await event.open_link(link_faq)