'''
    Event called when a member sends a message containing urls
'''

from __main__ import bot
from src.Bot import Bot
bot: Bot

import discord

async def on_link( message: discord.Message, urls: list[str] ):
    pass
