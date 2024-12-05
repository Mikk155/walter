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
    __data__["name"] = "Say something";
    __data__["description"] = "Makes the bot say something"

    g_Sentences.push_back( "member_say" );

    # Return data for g_PluginManager
    return __data__;

@bot.tree.command()
@app_commands.guild_only()
@app_commands.describe(
    message='Say something',
    user='User to use identity',
)
async def say( interaction: discord.Interaction, message: str, user: typing.Optional[discord.Member] = None ):
    """Make the bot say something"""

    await interaction.response.defer( thinking=True, ephemeral=True );

    try:

        if not user:
            user = bot.user;

        avatar = user.avatar.url if user.avatar else None;
        username = user.display_name;

        webhook = await interaction.channel.create_webhook( name='say_cmd' );

        if webhook:

            said = await webhook.send( content=message, username=username, avatar_url=avatar );

            await webhook.delete()

            if said:

                CLogger( __name__ ).info(
                    "member_say.said",
                    [
                        interaction.user.global_name,
                        said.jump_url
                    ],
                    server=interaction.guild_id
                );

    except Exception as e:

        await bot.exception_handle( e, interaction=interaction );
