from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

@bot.event
@bot.exception
async def on_member_join( member : discord.Member ) -> None:
#
    pass;
#
