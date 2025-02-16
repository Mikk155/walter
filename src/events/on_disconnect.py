'''
    Event called when the bot disconnects from discord
'''

from __main__ import bot
from src.Bot import Bot
bot: Bot

import discord

@bot.event
async def on_disconnect():
    pass
