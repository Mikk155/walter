'''
    Event called when a member reply to a message
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

async def on_reply( message: discord.Message, replied: discord.Message ):

    from src.utils.utils import g_Utils

    try:

        ''''''

    except Exception as e:

        bot.exception( f"on_reply: {e}", message );
