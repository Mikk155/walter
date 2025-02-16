'''
    Event called when a sticker is updated
'''

from __main__ import bot

import discord

@bot.event
async def on_guild_stickers_update( guild: discord.Guild, before: list[discord.Sticker], after: list[discord.Sticker] ):
    pass
