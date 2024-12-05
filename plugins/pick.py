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

def on_initialization() -> dict:
    '''
    Called when the script is executed, this is the first hook ever called.

    The bot is not even initialized yet.

    This hook is required on all plugins and must return data.
    '''

    # Create data for g_PluginManager
    __data__: dict = {};
    __data__["name"] = "Bot chooses";
    __data__["description"] = "Let the bot decide something for you"

    g_Sentences.push_back( 'pick' );

    # Return data for g_PluginManager
    return __data__;

@bot.tree.command()
@app_commands.guild_only()
@app_commands.describe( options='Separate options by using comas' )
async def pick( interaction: discord.Interaction, options: str ):
    """Make the bot decide a option for you"""

    await interaction.response.defer( thinking=True );

    try:

        items = options.split( ',' );

        if len( items ) > 1:

            await interaction.followup.send(
                g_Format.brackets(
                    g_Sentences.get(
                        "pick.done",
                        interaction.guild_id
                    ),
                    [
                        ''.join( f'\n- {i}' for i in items ),
                        items[ random.randint( 0, len( items ) - 1 ) ]
                    ]
                )
            );

        else:

            await interaction.followup.send( g_Sentences.get( "pick.option", interaction.guild_id ) );

    except Exception as e:

        await bot.exception_handle( e, interaction=interaction );
