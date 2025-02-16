'''
    Event called when a member is typing
'''

from __main__ import bot
from src.Bot import Bot
bot: Bot

import discord
import datetime

@bot.event
async def on_typing( channel: discord.abc.Messageable, user: discord.Member | discord.User, when: datetime.datetime ):
    pass
