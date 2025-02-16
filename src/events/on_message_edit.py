'''
    Event called when a member edits a message
'''

from __main__ import bot
from src.Bot import Bot
bot: Bot

import discord

@bot.event
async def on_message_edit( before: discord.Message, after: discord.Message ):
    pass
