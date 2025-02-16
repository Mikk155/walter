'''
    Event called when a member adds/removes a reaction
'''

from __main__ import bot
from src.Bot import Bot
bot: Bot

import discord

class ReactionAction:
    removed = 0;
    added = 1;

async def on_reaction( reaction: discord.Reaction, user : discord.User, action: ReactionAction ):
    pass
