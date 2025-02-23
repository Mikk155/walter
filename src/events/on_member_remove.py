'''
    Event called when a member leaves a guild
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

@bot.event
async def on_member_remove( member : discord.Member ):

    from src.utils.sentences import sentences
    from src.utils.utils import g_Utils;

    try:

        if member.guild:

            if member.guild.id == g_Utils.Guild.LimitlessPotential:

                users_channel = bot.get_channel( g_Utils.Guild.Channel_Users );

                if users_channel:

                    embed = discord.Embed( color = discord.Color(0xda00ff), title=member.global_name, \
                                    description = sentences[ "MEMBER_LEFT" ].format( member.mention ) ); #-TODO Pass if baned/kicked + reason

                    embed.add_field( inline = False, name =sentences[ "MEMBER_SINCE" ], value = f'{member.joined_at.day}/{member.joined_at.month}/{member.joined_at.year}' );

                    await users_channel.send( embed=embed );

    except Exception as e:

        bot.exception( f"on_member_remove: {e}", member );
