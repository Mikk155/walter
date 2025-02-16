'''
    Event called when a member leaves a guild
'''

from __main__ import bot
from src.Bot import Bot
bot: Bot

import discord

@bot.event
async def on_member_remove( member : discord.Member ):
    pass
