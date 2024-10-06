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

@bot.tree.command()
@app_commands.describe(
    options='Separate options by using comas',
)
async def pick( interaction: discord.Interaction, options: str ):
    """Make the bot decide a option for you"""

    try:

        items = options.split( ',' );

        if len( items ) > 1:

            option = str( items[ random.randint( 0, len( items ) - 1 ) ] );

            await interaction.response.send_message( "From {}\nI choose.... {}".format( options, option.strip( " " ) ) );

        else:

            await interaction.response.send_message( "You have to provide at least two options", ephemeral=True );

    except Exception as e:

        await interaction.response.send_message( "Exception: {}".format( e ), ephemeral=True );
