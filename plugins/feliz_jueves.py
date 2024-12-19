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
    __data__["name"] = "Feliz jueves";
    __data__["description"] = "Reminder everyone that today is jueves";
    __hooks__: list[Hooks] = [ Hooks.on_think_day ];
    __data__["hooks"] = __hooks__;

    # Return data for g_PluginManager
    return __data__;

@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
@app_commands.describe( channel='Channel to use' )
async def cfg_felizjueves( interaction: discord.Interaction, channel: discord.TextChannel ):
    """Configure a channel to get feliz jueves every thursday"""

    await interaction.response.defer( thinking=True );

    try:

        cache = g_Cache.get();

        cache[ str(interaction.guild_id) ] = channel.id;

        await interaction.followup.send(
            g_Sentences.get(
                "channel_configured",
                interaction.guild_id,
                [
                    channel.jump_url
                ]
            )
        );

    except Exception as e:

        await bot.exception_handle( e, interaction=interaction );

async def on_think_day( guild: discord.Guild ) -> int:

    date = datetime.datetime.now();

    if date.isoweekday() != JUEVES:

        return HOOK_CONTINUE();

    cache = g_Cache.get();

    if str( guild.id ) in cache:

        randoms = [
            "https://youtu.be/BvtUSsok4JA?si=ybKl3D8CX7aI5KAq",
            "https://youtu.be/J9PHO6ZgW0Q?si=ID2WRe8Z9_PShFAV",
            "https://www.youtube.com/watch?v=M1FcoVImTwk",
            "https://youtu.be/2gBFVGgknNg?si=tmWmrb-VRhMfWDja",
            "https://youtu.be/E51pvhXgrHI?si=nfMXPlUuY6ER2WUd"
        ];

        url = randoms[ random.randint( 0, len( randoms ) - 1 ) ] if random.randint( 0, 100 ) > 80 else 'https://youtu.be/K0R9PIWiOuM?si=Gq-uORr1nGLnN6Ww';

        channel = bot.get_channel( cache[ str( guild.id ) ] );

        if channel:

            await channel.send( url );

    return HOOK_CONTINUE();
