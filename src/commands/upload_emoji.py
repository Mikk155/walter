from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import io
import os
import aiohttp
import discord
from PIL import Image
from discord import app_commands;

from src.utils.fmt import fmt

@bot.tree.command()

@app_commands.guild_only()

@app_commands.default_permissions( administrator=True )

@app_commands.describe( name= 'Emoji name', file='Emoji to upload' )

async def upload_emoji( interaction: discord.Interaction, name: str, file: discord.Attachment ):

    """Upload an emoji to the Bot's Host for rotating them every week"""

    await interaction.response.defer( thinking=True );

    try:

        if not file.filename.lower().endswith( ( '.png', '.jpg', '.jpeg', '.gif' ) ):

            await interaction.followup.send( "❌ The file must be a PNG, JPG or GIF." )

            return

        if file.size > 256 * 1024:

            await interaction.followup.send( "❌ The file is above the 256 KB size limit." )

            return

        async with aiohttp.ClientSession() as session:

            async with session.get( file.url ) as resp:

                if resp.status != 200:

                    await interaction.followup.send( "❌ Couldn't download the file." );

                    return

                data = await resp.read();

        if not file.filename.lower().endswith( '.gif' ):

            try:

                image = Image.open( io.BytesIO( data ) );

                if image.width > 128 or image.height > 128:

                    await interaction.followup.send(f"⚠️ The image is {image.width}x{image.height}. it should be ≤128x128." );

                return;

            except Exception as e:

                await interaction.followup.send( f"❌ The file is not a valid image: {e}" );

                return;

        extension = file.filename.lower();

        extension = extension[ extension.rfind( "." ) + 1 : ];

        if os.path.exists( fmt.join( f"emojis/{name}.{extension}" ) ):

            await interaction.followup.send( f"❌ A emoji named {name}.{extension} already exists." );

            return;

        with open( fmt.join( f"emojis/{name}.{extension}" ), 'wb') as f:

            f.write( data );

        await interaction.followup.send( f"Uploaded {name}.{extension}" );

    except Exception as e:

        embed = bot.exception( f"command::upload_emoji: {e}", interaction );

        await interaction.followup.send( embed=embed );
