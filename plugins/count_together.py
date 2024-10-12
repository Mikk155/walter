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
async def cfg_counttogether( interaction: discord.Interaction, channel: discord.TextChannel ):
    """Configure a channel as a count-together channel"""

    try:

        if interaction.user.guild_permissions.administrator:

            cache = gpGlobals.cache.get();

            cache[ str(interaction.guild_id) ] = channel.id;

            await interaction.response.send_message( AllocString( "count.set" , [ channel.name ], interaction.guild_id ) );

        else:

            await interaction.response.send_message( AllocString( "no.permission", [ "administrator" ], interaction.guild_id ) );

    except Exception as e:

        await interaction.response.send_message( f"Exception: {e}" );

def get_count_number( string: str ):

    num = re.search( r'\b(\d+)\b', string );

    if num:

        return int( num.group(1) );

    return 0;

async def on_message( message: discord.Message ):

    if gpGlobals.developer():
        return Hook.Continue();

    if message.author.id == bot.user.id: # Nothing to do in this channel. Handle
        return Hook.Handled();

    cache = gpGlobals.cache.get();

    if not message.guild or not str( message.guild.id ) in cache:
        return Hook.Continue();

    channel_id = cache.get( str( message.guild.id ) );

    if not message.channel or channel_id != message.channel.id:
        return Hook.Continue();

    numero_actual = get_count_number( message.content );

    if numero_actual <= 0:

        await message.reply( AllocString( "count.only.count", [ message.author.mention ], message.guild.id ), delete_after = 5, silent=True, mention_author=False );

        await message.delete();

        return Hook.Handled();

    async for old_message in message.channel.history( limit=10, before=message.created_at ):

        if message.id == old_message.id:
            continue;

        numero_anterior = get_count_number( old_message.content );

        if numero_anterior > 0 and numero_actual - 1 != numero_anterior:

            await message.channel.send( AllocString( "count.wrong.count", [ message.author.mention ], message.guild.id ), delete_after = 5, silent=True, mention_author=False );

            await message.delete();

            return Hook.Handled();

async def on_daily():

    if gpGlobals.developer():
        return Hook.Continue();

    cache = gpGlobals.cache.get();

    for guild, channel_id in cache.items():

        channel = bot.get_channel( channel_id );

        if not channel:
            cache.pop( guild, '' ); # Pop out
            continue;

        async for old_message in channel.history( limit=10 ):

            if old_message.author == bot.user:

                break;

            numero_anterior = get_count_number( old_message.content )

            if numero_anterior > 0:

                msg = str( numero_anterior + 1 );

                await channel.send( msg );
