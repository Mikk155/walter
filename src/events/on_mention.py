'''
    Event called when a member mentions someone
'''

from __main__ import bot

import discord

async def on_mention( message: discord.Message, mentions: list[ discord.User | discord.Member ]):
    pass
