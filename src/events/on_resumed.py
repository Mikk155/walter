'''
    Event called when the bot is reconnected.
    
    This is not called when it run for a first time.
'''

from __main__ import bot
from src.Bot import Bot
bot: Bot

import discord

async def on_resumed():
    bot.m_Logger.info( f"Connection restored." ) # -TODO Store timedelta?
