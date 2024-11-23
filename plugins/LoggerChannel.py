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
async def cfg_logger_channel( interaction: discord.Interaction, channel: discord.TextChannel ):
    """Configure a channel to get loggers"""

    try:

        if interaction.user.guild_permissions.administrator:

            await bot.log_server_set( interaction.guild_id, channel.id );

            await interaction.response.send_message( AllocString( "logger.set" , [ channel.name ], interaction.guild_id ) );

        else:

            await interaction.response.send_message( AllocString( "no.permission", [ "administrator" ], interaction.guild_id ) );

    except Exception as e:

        await interaction.response.send_message( f"Exception: {e}" );

async def on_message_delete( message: discord.Message ):

    if message.guild:
        await bot.log_server( 'Message sent by ``{}`` deleted in <#{}>\n- {}', message.guild.id, [ message.author.name, message.channel.id, message.content ] );

    return Hook.Continue();

async def on_message_edit( before: discord.Message, after: discord.Message ):

    if not after.guild:
        return Hook.Continue();

    old = before.content;
    new = after.content;

    matcher = difflib.SequenceMatcher(None, old, new)
    old_result = []
    new_result = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            old_result.append(old[i1:i2])
            new_result.append(new[j1:j2])
        elif tag == 'replace':
            old_result.append(f"``{old[i1:i2]}``")
            new_result.append(f"``{new[j1:j2]}``")
        elif tag == 'delete':
            old_result.append(f"``{old[i1:i2]}``")
        elif tag == 'insert':
            new_result.append(f"``{new[j1:j2]}``")

    old = ''
    new = ''
    for o in old_result:
        old += o;
    for n in new_result:
        new += n;

    await bot.log_server( 'Message sent by ``{}`` edited in <#{}>\n- old: {}\n- new: {}', after.guild.id, [ after.author.name, after.channel.id, old, new ] );

    return Hook.Continue();
