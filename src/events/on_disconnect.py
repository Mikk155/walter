'''
    Event called when the bot disconnects from discord
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

@bot.event
async def on_disconnect():

    from src.utils.utils import g_Utils

    if g_Utils.developer:
        return;

    try:

        ''''''

    except Exception as e:

        bot.exception( f"on_disconnect: {e}" );
