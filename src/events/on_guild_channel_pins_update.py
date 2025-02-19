'''
    Event called when a message is pinned
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;
import datetime;

@bot.event
async def on_guild_channel_pins_update( channel: discord.TextChannel | discord.Thread, last_pin: datetime.datetime ):

    try:

        ''''''

    except Exception as e:

        bot.exception( f"on_guild_channel_pins_update: {e}", channel );
