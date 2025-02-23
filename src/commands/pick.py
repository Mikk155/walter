from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import random
import discord
from discord import app_commands;

from typing import Optional;

from src.utils.sentences import sentences

@bot.tree.command()

@app_commands.guild_only()

@app_commands.describe( options='Separate options by using comas' )

async def pick( interaction: discord.Interaction, options: str ):

    """Make the bot decide a option for you"""

    await interaction.response.defer( thinking=True );

    try:

        items = options.split( ',' );

        if len( items ) > 1:

            await interaction.followup.send( sentences[ "PICK_DONE" ].format( ''.join( f'\n- {i}' for i in items ), items[ random.randint( 0, len( items ) - 1 ) ] ) );

        else:

            await interaction.followup.send( sentences[ "PICK_OPTIONS" ], ephemeral=True );

    except Exception as e:

        embed = bot.exception( f"command::pick: {e}", interaction );

        await interaction.followup.send( embed=embed );
