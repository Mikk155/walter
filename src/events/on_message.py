from __main__ import bot
from typing import List;
from src.Bot import Bot;
bot: Bot;

import discord;

@bot.event
@bot.exception
async def on_message( message: discord.Message ) -> None:
#
    content: str = message.content;

    if content.find( "https://" ) != -1 or content.find( "www." ) != -1:
    #
        pass;
    #

    replied: discord.MessageReference | None = message.reference;

    if replied is not None:
    #
        pass;
    #

    mentions: List[discord.User | discord.Member] = message.mentions;

    if len( mentions ) > 0:
    #
        pass;
    #
#
