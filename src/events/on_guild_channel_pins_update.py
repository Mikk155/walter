'''
    Event called when a message is pinned
'''

from __main__ import bot

import discord
import datetime

@bot.event
async def on_guild_channel_pins_update( channel: discord.TextChannel | discord.Thread, last_pin: datetime.datetime ):
    pass
