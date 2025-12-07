from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;
from discord.ext.tasks import loop;

@loop( seconds = 1.0, reconnect=True, name="on_think" )
@bot.exception
async def on_think() -> None:
#
    await bot.wait_until_ready()
#
