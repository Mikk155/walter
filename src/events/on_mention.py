'''
    Event called when a member mentions someone
'''

from __main__ import bot
from src.Bot import Bot
bot: Bot

import discord

from src.utils.CCacheManager import g_Cache

async def on_mention( message: discord.Message, mentions: list[ discord.User | discord.Member ]):

    try:

        cache = g_Cache.get( "ping_counter");

        for user in mentions:
            if user:
                counts = cache.get( f'<@{user.id}>', [ 0, user.global_name ] );
                counts[1] = user.global_name;
                counts[0] = counts[0] + 1;
                cache[ f'<@{user.id}>' ] = counts;

    except Exception as e:

        bot.exception( f"on_mention: {e}", message )
