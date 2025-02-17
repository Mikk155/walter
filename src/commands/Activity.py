
from __main__ import bot
from src.Bot import Bot
bot: Bot

import io
import json
import aiohttp
import discord
from discord import app_commands

from src.utils.CCacheManager import g_Cache
from typing import Optional

@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions( administrator=True )
@app_commands.describe( new_activity='New Actiivity json file to replace.' )
async def activity( interaction: discord.Interaction, new_activity: Optional[discord.Attachment] = None ):
    """Upload or set the bot's Activity status json"""

    await interaction.response.defer( thinking=True )

    try:

        if new_activity:

            if not new_activity.filename.endswith( '.json' ):
                await interaction.followup.send( bot.sentences.get( "ONLY_FORMAT_SUPPORT", "json" ) )
                return

            async with aiohttp.ClientSession() as session:

                async with session.get( new_activity.url ) as response:

                    if response.status == 200:

                        data_bytes = await response.read()

                        try:
                            data = json.loads( data_bytes )
                            g_Cache.set( "Activity", data )
                        except Exception as e:
                            await interaction.followup.send( bot.sentences.get( "INVALID_JSON_OBJECT", e ) )
                            return

                        await interaction.followup.send( bot.sentences.get( "UPDATED_FILE" ) )

                    else:
                        await interaction.followup.send( bot.sentences.get( "FAIL_DOWNLOAD_FILE" ) )
        else:

            cache = g_Cache.get( "Activity" )

            emoji_list = json.dumps( cache, indent=0 )

            buffer = io.BytesIO( emoji_list.encode( 'utf-8' ) )

            buffer.seek(0)

            await interaction.followup.send( file=discord.File( buffer, "json.json" ) )

    except Exception as e:

        await bot.exception( f"command::activity: {e}" )
