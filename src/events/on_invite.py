from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;
from src.const import TheCult, LimitlessPotential;

@bot.event
@bot.exception
async def on_invite_delete( invite: discord.Invite )-> None:
#
    TheCult.Invites.pop( invite.code, None );
    LimitlessPotential.Invites.pop( invite.code, None );
#

@bot.event
@bot.exception
async def on_invite_create( invite: discord.Invite )-> None:
#
    if invite.guild:
    #
        if invite.guild == LimitlessPotential.id:
        #
            LimitlessPotential.Invites[ invite.code ] = invite.uses;
        #
        elif invite.guild == TheCult.id:
        #
            TheCult.Invites[ invite.code ] = invite.uses;
        #
    #
#
