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

@bot.tree.command( guild=bot.get_guild( gpGlobals.LimitlessPotential.server_id() ) )
@app_commands.describe(
    title='Meme Title',
    url='Meme url (Leave empty for removing a meme from the list)',
)
async def cfg_meme( interaction: discord.Interaction, title: str, url: str = None ):
    """Reposts a meme"""

    try:

        if interaction.user.guild_permissions.administrator:

            cache = gpGlobals.cache.get();

            if url:

                cache[ title ] = url;

                await interaction.response.send_message( AllocString( "item.added" , [ url ], interaction.guild_id ) );

            else:

                cache.pop( title, '' )
                cache.update();

                await interaction.response.send_message( AllocString( "item.removed" , [ url ], interaction.guild_id ) );

        else:

            await interaction.response.send_message( AllocString( "no.permission", [ "administrator" ], interaction.guild_id ) );

    except Exception as e:

        await interaction.response.send_message( f"Exception: {e}" );

class MemeDropdown( discord.ui.Select ):

    message = '';

    def __init__( self, server_id, message ):

        self.message = message;

        cache = gpGlobals.cache.get();

        options = [ discord.SelectOption( label=meme ) for meme in cache.keys() ];

        super().__init__( placeholder=AllocString( "meme.choose", [], server_id ), min_values=1, max_values=1, options=options );

    async def callback( self, interaction: discord.Interaction ):

        try:
            cache = gpGlobals.cache.get();

            choice = self.values[0];

            meme_url = cache[ choice ];

            avatar = interaction.user.avatar.url if interaction.user.avatar else None;
            username = interaction.user.display_name;

            webhook = await interaction.channel.create_webhook( name='meme_interface' );

            await interaction.response.send_message( choice, ephemeral=True, delete_after=0.1 );

            await webhook.send( content="[{}]({})".format( self.message if self.message else choice, meme_url ), username=username, avatar_url=avatar );

            await webhook.delete()

        except:
            pass

class MemeView( discord.ui.View ):

    def __init__( self, server_id, message ):

        super().__init__();

        self.add_item( MemeDropdown( server_id, message ) );

@bot.tree.command()
@app_commands.describe(
    message='Additional optional message',
)
async def meme( interaction: discord.Interaction, message:str = None ):
    """Open the memes interface"""

    try:

        embed = discord.Embed( title="Meme Interface", description=AllocString( "meme.choose", [], interaction.guild_id ) );

        await interaction.response.send_message( embed=embed, view=MemeView( interaction.guild_id, message ), ephemeral=True );

    except Exception as e:

        await bot.handle_exception( interaction, e );
