from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

@bot.event
@bot.exception
async def on_message_edit( before: discord.Message, after: discord.Message ) -> None:
#
    pass;
#
