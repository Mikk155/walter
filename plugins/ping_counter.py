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

async def on_mention( message: discord.Message, mentions: list[ discord.Member | discord.User ] ):

    for user in mentions:

        mention = gpUtils.mention( user );

        counts = json.load( open( '{}ping_counter.json'.format( gpGlobals.absp() ), 'r' ) );

        counts[ mention ] = [ counts[ mention ][ 0 ] + 1 if mention in counts else 1, user.global_name ];

        open( '{}ping_counter.json'.format( gpGlobals.absp() ), 'w' ).write( json.dumps( counts, indent=1));

    return Hook.Continue();

@bot.tree.command()
@app_commands.describe(
    user='Member',
)
async def ping_count( interaction: discord.Interaction, user: discord.Member ):
    """Show how many times a user has been pinged"""

    try:

        user_mentioned = gpUtils.mention( user );

        counts = json.load( open( '{}ping_counter.json'.format( gpGlobals.absp() ), 'r' ) );

        if user_mentioned in counts:
            times = 0 if not user_mentioned in counts else counts[ user_mentioned ][ 0 ]

            await interaction.response.send_message( "The user {} has been pinged {} times <:pingreee:911150900666572842>".format( counts[ user_mentioned ][ 1 ], times ))

        else:

            await interaction.response.send_message( "The user {} has not been pinged yet, This is the first <:pingreee:911150900666572842>".format( user.mention ))

    except Exception as e:

        await interaction.response.send_message( f"Exception {e}", ephemeral=True );
