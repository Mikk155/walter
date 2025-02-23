'''
    Event called when the bot is run for the first time.
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

async def on_start():

    from src.utils.utils import g_Utils

    try:

        ''''''

    except Exception as e:

        bot.exception( f"on_start: {e}" );
