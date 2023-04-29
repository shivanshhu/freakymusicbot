from pyrogram import filters
from pyrogram.types import Message

from Freaky.utilities.config import BANNED_USERS
from Freaky.utilities.strings import get_command
from Freaky import bot
from Freaky.modules.database import set_cmode
from Freaky.modules.decorators.admins import AdminActual

### Multi-Lang Commands
CHANNELPLAY_COMMAND = get_command("CHANNELPLAY_COMMAND")


@bot.on_message(
    filters.command(CHANNELPLAY_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminActual
async def playmode_(client, message: Message, _):
    if len(message.command) < 2:
        return await message.reply_text(
            _["cplay_1"].format(
                message.chat.title, CHANNELPLAY_COMMAND[0]
            )
        )
    query = message.text.split(None, 2)[1].lower().strip()
    if (str(query)).lower() == "disable":
        await set_cmode(message.chat.id, None)
        return await message.reply_text("Channel Play Disabled")
    elif str(query) == "linked":
        chat = await bot.get_chat(message.chat.id)
        if chat.linked_chat:
            chat_id = chat.linked_chat.id
            await set_cmode(message.chat.id, chat_id)
            return await message.reply_text(
                _["cplay_3"].format(
                    chat.linked_chat.title, chat.linked_chat.id
                )
            )
        else:
            return await message.reply_text(_["cplay_2"])
    else:
        try:
            chat = await bot.get_chat(query)
        except:
            return await message.reply_text(_["cplay_4"])
        if chat.type != "channel":
            return await message.reply_text(_["cplay_5"])
        try:
            admins = await bot.get_chat_members(
                chat.id, filter="administrators"
            )
        except:
            return await message.reply_text(_["cplay_4"])
        for users in admins:
            if users.status == "creator":
                creatorusername = users.user.username
                creatorid = users.user.id
        if creatorid != message.from_user.id:
            return await message.reply_text(
                _["cplay_6"].format(chat.title, creatorusername)
            )
        await set_cmode(message.chat.id, chat.id)
        return await message.reply_text(
            _["cplay_3"].format(chat.title, chat.id)
        )