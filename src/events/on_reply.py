'''
    Event called when a member reply to a message
'''

from __main__ import bot
from src.Bot import Bot
bot: Bot

import discord

async def on_reply( message: discord.Message, replied: discord.Message ):
    pass
