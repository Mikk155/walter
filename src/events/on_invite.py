'''
    Event called when a invite is created/deleted
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

class InviteAction:
    deleted = 0;
    created = 1;

async def on_invite( invite: discord.Invite, action: InviteAction ):

    from src.utils.utils import g_Utils

    try:

        if invite.guild:

            if invite.guild.id == g_Utils.Guild.LimitlessPotential:

                await bot.update_invites();

    except Exception as e:

        bot.exception( f"on_invite: {e}" );
