from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;
from discord import app_commands;

from src.utils.sentences import sentences
from src.utils.CCacheManager import g_Cache;
from typing import Optional;

@bot.tree.command()

@app_commands.guild_only()

@app_commands.describe( user='Member' )

async def ping_count( interaction: discord.Interaction, user: Optional[discord.Member] = None ):

    """Show how many times a user has been pinged"""

    await interaction.response.defer( thinking=True );

    try:

        if user is None or not user:

            user = interaction.user;

        if user:

            cache = g_Cache.get( "ping_counter");

            counts = cache.get( f'<@{user.id}>', [ 0, user.global_name ] );

            if counts[0] > 0:

                await interaction.followup.send( sentences[ "PING_COUNTER_TIMES" ].format( counts[1], counts[0] ) );

            else:

                await interaction.followup.send( sentences[ "PING_COUNTER_FIRST" ].format( f'<@{user.id}>' ) );

                counts[0] = 1;

                counts[ f'<@{user.id}>' ] = counts;

    except Exception as e:

        embed = bot.exception( f"command::ping_count: {e}", interaction );

        await interaction.followup.send( embed=embed );
