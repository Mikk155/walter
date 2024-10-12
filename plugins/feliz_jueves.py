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
async def cfg_felizjueves( interaction: discord.Interaction, channel: discord.TextChannel ):
    """Configure a channel to get feliz jueves every thursday"""

    try:

        if interaction.user.guild_permissions.administrator:

            cache = gpGlobals.cache.get();

            cache[ str(interaction.guild_id) ] = channel.id;

            await interaction.response.send_message( AllocString( "feliz_jueves.set" , [ channel.name ], interaction.guild_id ) );

        else:

            await interaction.response.send_message( AllocString( "no.permission", [ "administrator" ], interaction.guild_id ) );

    except Exception as e:

        await interaction.response.send_message( f"Exception: {e}" );

async def on_daily():

    date = datetime.now();

    if date.isoweekday() != 4:
        return Hook.Continue();

    randoms = [
        "https://youtu.be/BvtUSsok4JA?si=ybKl3D8CX7aI5KAq",
        "https://youtu.be/J9PHO6ZgW0Q?si=ID2WRe8Z9_PShFAV",
        "https://www.youtube.com/watch?v=M1FcoVImTwk",
        "https://www.youtube.com/watch?v=vMkMi3DV1tM",
        "https://youtu.be/2gBFVGgknNg?si=tmWmrb-VRhMfWDja",
        "https://youtu.be/E51pvhXgrHI?si=nfMXPlUuY6ER2WUd"
    ];

    # Pick a random one in 20% chance
    url = randoms[ random.randint( 0, len( randoms ) - 1 ) ] if random.randint( 0, 100 ) > 80 else 'https://youtu.be/K0R9PIWiOuM?si=Gq-uORr1nGLnN6Ww';

    cache = gpGlobals.cache.get();

    for guild, channel_id in cache.items():

        channel = bot.get_channel( channel_id );

        if not channel:
            cache.pop( guild, '' ); # Pop out
            continue;

        await channel.send( url );
