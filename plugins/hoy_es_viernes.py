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
async def cfg_hoyesviernes( interaction: discord.Interaction, channel: discord.TextChannel ):
    """Configure a channel to get hoy es viernes"""

    try:

        if interaction.user.guild_permissions.administrator:

            cache = gpGlobals.cache.get();

            cache[ str(interaction.guild_id) ] = channel.id;

            await interaction.response.send_message( AllocString( "viernes.set" , [ channel.name ], interaction.guild_id ) );

        else:

            await interaction.response.send_message( AllocString( "no.permission", [ "administrator" ], interaction.guild_id ) );

    except Exception as e:

        await interaction.response.send_message( f"Exception: {e}" );

async def on_daily():

    date = datetime.now();

    if date.isoweekday() != 5:
        return Hook.Continue();

    randoms = [
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

    cache = gpGlobals.cache.get();

    for guild, channel_id in cache.items():

        channel = bot.get_channel( channel_id );

        if not channel:
            cache.pop( guild, '' ); # Pop out
            continue;

        await channel.send( url );
