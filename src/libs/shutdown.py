from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;
from src.const import MikkID;
from discord import app_commands;

@bot.tree.command()
@app_commands.guild_only()
@bot.exception
async def shutdown( interaction: discord.Interaction, ) -> None:
#
    """Shutdown the bot"""

    if interaction.user.id != MikkID:
    #
        await interaction.response.send_message( "Only mikk can turn me off >.<" );
    #
    else:
    #
        await interaction.response.send_message( "Shutting down..." );
        exit(0);
    #
#
