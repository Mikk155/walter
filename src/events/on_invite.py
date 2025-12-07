from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

@bot.event
@bot.exception
async def on_invite_delete( invite: discord.Invite )-> None:
#
    pass;
#

@bot.event
@bot.exception
async def on_invite_create( invite: discord.Invite )-> None:
#
    pass;
#
