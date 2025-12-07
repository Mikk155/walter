from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

@bot.event
@bot.exception
async def on_reaction_add( reaction: discord.Reaction, user : discord.User ) -> None:
#
    pass;
#

@bot.event
@bot.exception
async def on_reaction_remove( reaction: discord.Reaction, user : discord.User ) -> None:
#
    pass;
#
