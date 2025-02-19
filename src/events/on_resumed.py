'''
    Event called when the bot is reconnected.
    
    This is not called when it run for a first time.
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

async def on_resumed():

    bot.m_Logger.info( f"Connection restored." ).print() # -TODO Store timedelta?

    try:

        ''''''

    except Exception as e:

        bot.exception( f"on_resumed: {e}" );
