'''
    Event called when the bot disconnects from discord
'''

from __main__ import bot
from src.Bot import Bot
bot: Bot

import discord

@bot.event
async def on_disconnect():

    try:

        ''''''

    except Exception as e:

        bot.exception( f"on_disconnect: {e}" )
