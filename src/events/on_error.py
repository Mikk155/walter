'''
    Event called when a unhandled exception raised
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

#@bot.event
async def on_error( event: str, *args, **kwargs ):

    from src.utils.utils import g_Utils

    try:

        ''''''

    except Exception as e:

        bot.exception( f"event: {e}" );
