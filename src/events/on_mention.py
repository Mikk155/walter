'''
    Event called when a member mentions someone
'''

from __main__ import bot
from src.Bot import Bot
bot: Bot

import discord

async def on_mention( message: discord.Message, mentions: list[ discord.User | discord.Member ]):
    pass
