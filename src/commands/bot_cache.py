"""
The MIT License (MIT)

Copyright (c) 2024 Mikk155

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from src.main import *

@bot.tree.command()
@app_commands.describe( json='New Cache json object file' )
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
@app_commands.describe(
    json='json object containing the cache to upload.',
)
async def cfg_cache( interaction: discord.Interaction, json: discord.Attachment ):
    """Update the bot cache"""

    await interaction.response.defer( thinking=True );

    try:

        if not json.filename.endswith( '.json' ):

            await interaction.followup.send( g_Sentences.get( "cache.update.file.nojson", interaction.guild_id ) );

        elif interaction.user.id != g_Config.configuration[ "owner_id" ]:

            await interaction.followup.send(
                g_Format.brackets(
                    g_Sentences.get(
                        "only.owner",
                        interaction.guild_id
                    ) ) [
                    g_Config.configuration[ "owner_id" ]
                ]
            );

        else:

            await interaction.followup.send( g_Sentences.get( "cache.update.file.updating", interaction.guild_id ) );

            async with aiohttp.ClientSession() as session:

                async with session.get( json.url ) as response:

                    if response.status == 200:

                        data = await response.read();

                        with open( g_Path.join( "cache.json" ), "wb") as f:

                            f.write( data );

                        __json__ = jsonc.load( g_Path.join( "cache.json" ) );

                        g_Cache.__cache__ = __json__;

                        await interaction.followup.send( g_Sentences.get( "cache.update.updated.cache", interaction.guild_id ) );

                    else:

                        raise Exception( "Couldn't download the file." );

    except Exception as e:

        await bot.exception_handle( e, interaction=interaction );

@bot.tree.command()
async def cache( interaction: discord.Interaction ):
    """Gets the bot cache"""

    await interaction.response.defer( thinking=True );

    try:

        with open( g_Path.join( "cache.json" ), "rb") as file:

            await interaction.followup.send( "cache", file=discord.File( file, "data.json" ) );

    except Exception as e:

        await bot.exception_handle( e, interaction=interaction );
