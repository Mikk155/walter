'''
    Event called when a invite is created/deleted
'''

from __main__ import bot

import discord

class InviteAction:
    deleted = 0;
    created = 1;

async def on_invite( invite: discord.Invite, action: InviteAction ):
    pass
