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

from plugins.main import *

@bot.tree.command( guild=bot.get_guild( gpGlobals.LimitlessPotential.server_id ) )
@app_commands.describe(
    file='json object containing the cache to upload.',
)
async def cache( interaction: discord.Interaction, file: Optional[discord.Attachment] = None ):
    """Returns the bot cache for recovery purposes"""

    try:

        if file:

            if not file.filename.endswith( '.json' ):

                await interaction.response.send_message( AllocString( "only.{}.is.permited", [ f"``.json`` file"], interaction.guild_id ) );

            else:

                if interaction.user.id != gpGlobals.LimitlessPotential.mikk_id:

                    await interaction.response.send_message( AllocString( "only.owner", [], interaction.guild_id ) );

                    return;

                await interaction.response.send_message( AllocString( "updating.cache", [], interaction.guild_id ));

                async with aiohttp.ClientSession() as session:

                    async with session.get( file.url ) as response:

                        if response.status == 200:

                            data = await response.read();

                            with open( "{}/cache.json".format( gpGlobals.abs() ), "wb") as f:

                                f.write( data );

                            gpGlobals.cache = gpGlobals.CCacheManager( gpUtils.jsonc( 'cache.json' ) );

                            await interaction.channel.send( AllocString( "updated.cache", [], interaction.guild_id ) );

                        else:

                            raise Exception( "Couldn't download the file." );

        else:

            await interaction.response.send_message( AllocString( "packing.cache", [], interaction.guild_id ) );

            with open( "{}/cache.json".format( gpGlobals.abs() ), "rb") as file:

                await interaction.channel.send( "cache", file=discord.File( file, "data.json" ) );

    except Exception as e:

        await interaction.channel.send( "Exception: {}".format( e ) );
