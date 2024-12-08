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
    __data__["name"] = "Hoy es viernes";
    __data__["description"] = "Reminder everyone that today is viernes";
    __hooks__: list[Hooks] = [ Hooks.on_think_day ];
    __data__["hooks"] = __hooks__;

    # Return data for g_PluginManager
    return __data__;

@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
@app_commands.describe( channel='Channel to use' )
async def cfg_hoyesviernes( interaction: discord.Interaction, channel: discord.TextChannel ):
    """Configure a channel to get hoy es viernes"""

    await interaction.response.defer( thinking=True );

    try:

        cache = g_Cache.get();

        cache[ str(interaction.guild_id) ] = channel.id;

        await interaction.followup.send(
            g_Format.brackets(
                g_Sentences.get(
                    "channel.configured",
                    interaction.guild_id
                ),
                [
                    channel.jump_url
                ]
            )
        );

    except Exception as e:

        await bot.exception_handle( e, interaction=interaction );

async def on_think_day( guild: discord.Guild ) -> int:

    date = datetime.datetime.now();

    if date.isoweekday() != 7:

        return HOOK_CONTINUE();

    cache = g_Cache.get();

    if str( guild.id ) in cache:

        randoms = [
            "https://tenor.com/view/frieren-frieren-beyond-journey%27s-end-sousou-no-frieren-vrchat-friernes-gif-9517687105679474773",
            "https://youtu.be/aSUuw5HY9eY?si=7ysIS1UeXbKyCk3V",
            "https://youtu.be/_IN9q9tdHkQ?si=nMiOQm1oyUyyOOQl",
            "https://youtu.be/KRaZAStC-Tc?si=B2eDnRz5GWDr4hhq",
            "https://youtu.be/FkjQcbX-Ngk?si=fbK2PFv54QNBZp3k",
            "https://youtu.be/teRJKOPSRts?si=6IWnZ5OKC8i6xwWW",
            "https://youtu.be/PreudA3i6LI?si=YQNWiDAR2dIHzJhy",
            "https://youtu.be/ui7hcmy6Dsk?si=qnLRIGrjl1_uqXAx",
            "https://youtu.be/WLAlRCi8nz0?si=Q9HAd9JIl3IWvOcI",
            "https://youtu.be/HE1K1iUsNSo?si=Xg6wBDdEVlGs9x1O"
        ];

        url = randoms[ random.randint( 0, len( randoms ) - 1 ) ];

        channel = bot.get_channel( cache[ str( guild.id ) ] );

        if channel:

            await channel.send( url );

    return HOOK_CONTINUE();
