from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;
from discord import app_commands;

from src.utils.CCacheManager import g_Cache;
from typing import Optional;

@bot.tree.command( name = "cfg_birthday" )

@app_commands.guild_only()

@app_commands.default_permissions( administrator = True )

@app_commands.describe( json_file = 'New birthdays json file to replace.' )

async def birthday(
    interaction: discord.Interaction,
    user: Optional[discord.Member] = None,
    day: Optional[int] = None,
    month: Optional[int] = None,
    json_file: Optional[discord.Attachment] = None
):

    """Upload or set a member's birthday"""

    await interaction.response.defer( thinking=True );

    try:

        if json_file:

            json_object: tuple[ dict, discord.Embed ] = await bot.file_to_json( json_file );

            if json_object[0]:

                g_Cache.set( "birthdays", json_object[0] );

            if json_object[1]:

                await interaction.followup.send( embed = json_object[1] );

        elif user:

            if day and month:

                data = g_Cache.get( "birthdays" );

                data[ str(user.id) ] = [ day, month ];

                await interaction.followup.send( f"Set user {user.name} birthday to {day}/{month}", ephemeral=True );

            else:

                await interaction.followup.send( "You have to set a day and a month!", ephemeral=True );

        else:

            file: discord.File = bot.json_to_file( g_Cache.get( "birthdays" ) );

            await interaction.followup.send( file = file );

    except Exception as e:

        embed = bot.exception( f"command::activity: {e}", interaction );

        await interaction.followup.send( embed = embed );
