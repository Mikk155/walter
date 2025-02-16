'''
    Event called when a member joins a guild
'''

from __main__ import bot

import discord

@bot.event
async def on_member_join( member : discord.Member ):
    pass
