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

    __data__: dict = {};
    __data__["name"] = "Count together";
    __data__["description"] = "React with ❌ to messages that did a wrong count";
    __hooks__: list[Hooks] = [ Hooks.on_message ];
    __data__["hooks"] = __hooks__;

    return __data__;

@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
@app_commands.describe( channel='Channel', number='Last number sent in the channel' )
async def cfg_count_together(
    interaction: discord.Interaction,
    channel: typing.Optional[discord.TextChannel] = None,
    number: typing.Optional[int] = 1,
    disable: typing.Optional[bool] = None
):
    """Configure a channel as a count-together channel"""

    await interaction.response.defer( thinking=True );

    try:

        cache = g_Cache.get();

        cache[ str( interaction.guild_id ) ] = { "channel": channel.id, "number": number };

        await interaction.followup.send(
            g_Sentences.get(
                "disabled" if disable else "channel_configured",
                interaction.guild_id,
                [
                    channel.jump_url
                ]
            )
        );

    except Exception as e:

        await bot.exception_handle( e, interaction=interaction );

async def on_message( message: discord.Message ) -> int:

    if message.guild and message.content:

        cache = g_Cache.get();

        if str( message.guild.id ) in cache:

            data = cache.get( str( message.guild.id ), {} );

            if "channel" in data and data[ "channel" ] == message.channel.id:

                num = re.search( r'\b(\d+)\b', message.content );

                if num:

                    current = int( num.group(1) );

                    desired = data[ "number" ] + 1;

                    if desired != current:

                        await message.add_reaction( '❌' );

                    else:

                        data[ "number" ] = desired;

                        cache = data;

                else:

                    await message.add_reaction( '❌' );

    return HOOK_CONTINUE();
