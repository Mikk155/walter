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

global count_together_channels;
count_together_channels = gpUtils.jsonc( '{}count_together.json'.format( gpGlobals.absp() ) );

@bot.tree.command()
async def cfg_counttogether( interaction: discord.Interaction ):
    """Configure this channel as a count-together channel"""

    try:

        if interaction.user.guild_permissions.administrator:

            count_together_channels[ str(interaction.guild_id) ] = interaction.channel_id;

            open( '{}count_together.json'.format( gpGlobals.absp() ), 'w' ).write( json.dumps( count_together_channels, indent = 0 ) );

            await interaction.response.send_message( "Configuration set, Now only counting on this channel." );

        else:

            await interaction.response.send_message( "Only administrators can use this command.", ephemeral=True );

    except Exception as e:

        await interaction.response.send_message( f"Exception: {e}" );

async def on_message( message: discord.Message ):

    if not message.author or message.author.id == bot.user.id or not message.guild or not str(message.guild.id) in count_together_channels:

        return Hook.Continue();

    channel = bot.get_channel( int(count_together_channels[ str(message.guild.id) ]) );

    if not channel or message.channel is not channel:

        return Hook.Continue();

    numero_actual = re.search( r'\b(\d+)\b', message.content )

    if numero_actual:

        numero_actual = int( numero_actual.group(1) )

    else:

        await message.reply( f'{message.author.mention} Only counting on this channel!', delete_after = 5, silent=True, mention_author=False )

        await message.delete()

        return Hook.Handled();

    async for old_message in message.channel.history( limit=10, before=message.created_at ):

        if not old_message.content[0].isdigit():

            continue

        numero_anterior = re.search( r'\b(\d+)\b', old_message.content )

        if numero_anterior:

            numero_anterior = int(numero_anterior.group(1))

            break

    if numero_actual <= numero_anterior or numero_actual > numero_anterior + 1:

        await message.channel.send( f'{message.author.mention}, do you know how to count? :face_with_raised_eyebrow:', delete_after = 5, silent=True, mention_author=False )

        await message.delete()

        return Hook.Handled();

# -TODO on_daily
async def on_ready():

    for guild, channel_id in count_together_channels.items():

        channel = bot.get_channel( channel_id );

        if not channel:

            continue;

        numero_anterior = None;

        async for old_message in channel.history( limit=10 ):

            if old_message.author == bot.user:

                numero_anterior = None;

                break;

            if numero_anterior:

                continue

            if not old_message.content[0].isdigit():

                continue

            numero_anterior = re.search( r'\b(\d+)\b', old_message.content )

            if numero_anterior:

                numero_anterior = int(numero_anterior.group(1)) + 1

        if numero_anterior:

            await channel.send( f'{numero_anterior}')
