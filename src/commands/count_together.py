from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;
from discord import app_commands;

from src.utils.sentences import sentences
from src.utils.CCacheManager import g_Cache;

@bot.tree.command( name = "cfg_count_together" )

@app_commands.guild_only()

@app_commands.default_permissions( administrator = True )

@app_commands.describe( number = 'Last number sent in the channel' )

async def count_together( interaction: discord.Interaction, number: int ):

    """Update the last counter value"""

    await interaction.response.defer( thinking=True );

    try:

        cache = g_Cache.get( "count_together" );

        cache[ "number" ] = number;

        message = sentences[ "COUNT_TOGETHER_NUMBER" ].format( number );

        await interaction.followup.send( message );

        channel: discord.TextChannel = await bot.get_channel( 877493398070767636 );

        if channel:

            await channel.send( message );

    except Exception as e:

        embed = bot.exception( f"command::count_together: {e}", interaction );

        await interaction.followup.send( embed=embed );
