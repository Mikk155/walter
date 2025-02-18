
from __main__ import bot
from src.Bot import Bot
bot: Bot

import discord
from discord import app_commands

from src.utils.CCacheManager import g_Cache
from typing import Optional

@bot.tree.command( name="cfg_activity" )
@app_commands.guild_only()
@app_commands.default_permissions( administrator=True )
@app_commands.describe( new_activity='New Actiivity json file to replace.' )
async def activity( interaction: discord.Interaction, new_activity: Optional[discord.Attachment] = None ):
    """Upload or set the bot's Activity status json"""

    await interaction.response.defer( thinking=True )

    try:

        if new_activity:

            json_object = await bot.file_to_json( new_activity )

            if json_object[0]:
                g_Cache.set( "Activity", json_object[0] )
            if json_object[1]:
                await interaction.followup.send( embed=json_object[1] )
        else:

            await interaction.followup.send( file = bot.json_to_file( g_Cache.get( "Activity" ) ) )

    except Exception as e:

        await bot.exception( f"command::activity: {e}" )
