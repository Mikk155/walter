'''
    Event called when a emoji is updated
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

@bot.event
async def on_guild_emojis_update( guild: discord.Guild, before: list[discord.Emoji], after: list[discord.Emoji] ):

    try:

        ''''''

    except Exception as e:

        bot.exception( f"on_guild_emojis_update: {e}" );
