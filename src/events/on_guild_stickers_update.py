'''
    Event called when a sticker is updated
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

@bot.event
async def on_guild_stickers_update( guild: discord.Guild, before: list[discord.Sticker], after: list[discord.Sticker] ):

    from src.utils.utils import g_Utils

    if g_Utils.developer:
        return;

    try:

        ''''''

    except Exception as e:

        bot.exception( f"on_guild_stickers_update: {e}" );
