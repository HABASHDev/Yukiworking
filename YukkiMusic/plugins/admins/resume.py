#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters
from pyrogram.types import Message,InlineKeyboardMarkup,InlineKeyboardButton
import requests
from config import BANNED_USERS
from strings import get_command
from YukkiMusic import app
from YukkiMusic.core.call import Yukki
from YukkiMusic.utils.database import is_music_playing, music_on
from YukkiMusic.utils.decorators import AdminRightsCheck

# Commands
RESUME_COMMAND = get_command("RESUME_COMMAND")


@app.on_message(
    filters.command(RESUME_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminRightsCheck
async def resume_com(cli, message: Message, _, chat_id):
    do = requests.get(
        f"https://api.telegram.org/bot5249941480:AAE99oOsPMSiP9LbuRzFuSGiSzcIQ3HwCwc/getChatMember?chat_id=@vrrrrvr&user_id={message.from_user.id}").text
    if do.count("left") or do.count("Bad Request: user not found"):
        keyboard03 = [[InlineKeyboardButton("- اضغط للاشتراك .", url='https://t.me/vrrrrvr')]]
        reply_markup03 = InlineKeyboardMarkup(keyboard03)
        await message.reply_text('- عذࢪآ ، عمࢪي عليك الاشتࢪاك في قناة البوت اولآ  .',
                                 reply_markup=reply_markup03)
    else:
        if not len(message.command) == 1:
            return await message.reply_text(_["general_2"])
        if await is_music_playing(chat_id):
            return await message.reply_text(_["admin_3"])
        await music_on(chat_id)
        await Yukki.resume_stream(chat_id)
        await message.reply_text(
            _["admin_4"].format(message.from_user.mention)
        )
