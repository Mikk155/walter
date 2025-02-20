'''
    Event called when a member joins a guild
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

from src.utils.sentences import sentences
from src.utils.constants import guild_limitlesspotential_id

@bot.event
async def on_member_join( member : discord.Member ):

    try:

        if member.guild and member.guild.id == guild_limitlesspotential_id():

            await member.add_roles( member.guild.get_role( 1316214066384994324 ) );

            users_channel = bot.get_channel( 842174687445778483 );

            if users_channel:

                join_from = "global invite"; #-TODO Track down invites
                invited_by: discord.Member = None
                message_label = "MEMBER_JOINED_BY" if invited_by else "MEMBER_JOINED_FROM";

                embed = discord.Embed( color = discord.Color(0xda00ff), title=member.global_name, \
                                        description = sentences[ message_label ].format( member.mention, invited_by.name if invited_by else join_from ) )

                embed.add_field( inline = False, name = sentences[ "ACCOUNT_CREATION" ], \
                                value = f'{member.created_at.day}/{member.created_at.month}/{member.created_at.year}' );

                await users_channel.send( embed=embed );

    except Exception as e:

        bot.exception( f"on_member_join: {e}", member );
