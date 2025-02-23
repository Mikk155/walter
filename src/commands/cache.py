from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;
from discord import app_commands;

from src.utils.CCacheManager import g_Cache;
from typing import Optional;

@bot.tree.command( name = "cfg_cache" )

@app_commands.guild_only()

@app_commands.default_permissions( administrator = True )

@app_commands.describe( new_cache = 'New cache json file to replace.' )

async def cache( interaction: discord.Interaction, new_cache: Optional[discord.Attachment] = None ):

    """Upload or set the bot's cache json"""

    await interaction.response.defer( thinking=True );

    try:

        if new_cache:

            json_object: tuple[ dict, discord.Embed ] = await bot.file_to_json( new_cache );

            if json_object[0] and len(json_object[0]) > 0:

                g_Cache.__cache__ = g_Cache.CCacheDictionary( json_object[0] );

                file: discord.File = bot.json_to_file( g_Cache.__cache__ );

                await interaction.followup.send( "Old cache", file = file );

            if json_object[1]:

                await interaction.followup.send( embed = json_object[1] );

        else:

            file: discord.File = bot.json_to_file( g_Cache.__cache__ );

            await interaction.followup.send( file = file );

    except Exception as e:

        embed = bot.exception( f"command::cache: {e}", interaction );

        await interaction.followup.send( embed = embed );
