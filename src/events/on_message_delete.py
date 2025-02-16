'''
    Event called when a member deletes a message
'''

from __main__ import bot

import discord

@bot.event
async def on_message_delete( message: discord.Message ):
    pass
