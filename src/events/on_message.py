'''
    Event called when a member sends a message
'''

from __main__ import bot
from src.Bot import Bot
bot: Bot

import discord

async def on_message( message: discord.Message ):

    # Remove sent messages to #welcome #-TODO Should we use a button + vgui instead of a app command
    if message.guild.id == 744769532513615922 and message.channel.id == 1118352656096829530 and not message.author.guild_permissions.administrator:
        await message.delete();
