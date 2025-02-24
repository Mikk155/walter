from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord
from discord import app_commands;

from src.utils.CCacheManager import g_Cache

@bot.tree.command( name = "cfg_queue_members" )

@app_commands.guild_only()

@app_commands.default_permissions( administrator=True )

@app_commands.describe( user_id = 'User to queue' )

async def queue_members( interaction: discord.Interaction, user_id: str ):

    """Queue a user id to prevent the bot blocking his access to the channels for being a new user"""

    await interaction.response.defer( thinking=True );

    try:

        cache = g_Cache.get( "new_members" );

        queue = cache.get( "queue", [] );

        queue.append( user_id );

        cache[ "queue" ] = queue;

        await interaction.followup.send( "Queued member {} ID ``{}``".format( "<@{}>".format( user_id ), user_id ) );

    except Exception as e:

        embed = bot.exception( f"command::say: {e}", interaction );

        await interaction.followup.send( embed=embed );
