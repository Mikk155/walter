'''
    Event called when a member leaves a guild
'''

from __main__ import bot

import discord

@bot.event
async def on_member_remove( member : discord.Member ):
    pass
