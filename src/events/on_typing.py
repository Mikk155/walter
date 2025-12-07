from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;
from datetime import datetime;

@bot.event
@bot.exception
async def on_typing( channel: discord.abc.Messageable, user: discord.Member | discord.User, when: datetime ) -> None:
#
    pass;
#
