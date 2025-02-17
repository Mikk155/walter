'''
    Event called when a member leaves a guild
'''

from __main__ import bot
from src.Bot import Bot
bot: Bot

import discord

@bot.event
async def on_member_remove( member : discord.Member ):

    try:

        if member.guild.id == 744769532513615922:

            users_channel = bot.get_channel( 842174687445778483 )

            if users_channel:

                embed = discord.Embed( color = discord.Color(0xda00ff), title=member.global_name, description=f"{member.mention} left the server." );

                embed.add_field( inline = False, name ="Member since", value = f'{member.joined_at.day}/{member.joined_at.month}/{member.joined_at.year}' );

                await users_channel.send( embed=embed );

    except Exception as e:

        bot.exception( f"on_member_remove: {e}" )
