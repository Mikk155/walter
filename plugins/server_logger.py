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

    __data__: dict = {};
    __data__["name"] = "Server Logger";
    __data__["description"] = "Keep track of server events and log them";
    __data__["hooks"] = [
        Hooks.on_message_delete,
        Hooks.on_message_edit
    ];

    return __data__;

all_choices = {
    "Message Delete": "message_delete",
    "Message Edit": "message_edit",
};

@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
@app_commands.choices( logger = g_Format.to_command_choices( all_choices ) )
@app_commands.describe(
    logger='Logger type',
    channel='Text channel to display the log',
    remove='True removes the config'
)
async def cfg_server_logger(
    interaction: discord.Interaction,
    logger: app_commands.Choice[str],
    channel: typing.Optional[discord.TextChannel] = None,
    remove: bool = False
):
    """Configure Server Loggers"""

    await interaction.response.defer( thinking=True );

    try:

        cache = g_Cache.get();

        srv:dict = cache.get( str( interaction.guild_id ), {} );

        if remove:

            srv.pop( logger.value, None );

            await interaction.followup.send(
                g_Sentences.get(
                    "disabled",
                    interaction.guild_id
                )
            );

        else:

            srv[ logger.value ] = channel.id;

            await interaction.followup.send(
                g_Sentences.get(
                    "channel_configured",
                    interaction.guild_id,
                    [
                        channel.jump_url
                    ]
                )
            );

        cache[ str( interaction.guild_id ) ] = srv;

    except Exception as e:

        await bot.exception_handle( e, interaction=interaction );

def server_logger_channel( logger: str, id: int ) -> discord.TextChannel | None:

    cache = g_Cache.get();

    srv:dict = cache.get( str( id ), {} );

    if logger in srv:

        channel = bot.get_channel( srv[ logger ] );

        if channel:

            return channel;

    return None;

async def on_message_delete( message: discord.Message ) -> int:

    if message.author.id == bot.user.id:
        return HOOK_CONTINUE();

    if message.guild:

        channel = server_logger_channel( "message_delete", message.guild.id );

        if channel:

            embed = discord.Embed(
                color = 16711680
            );

            embed.add_field( inline = False,
                name = message.author.name,
                value = "Message sent by {} deleted in {}".format( message.author.mention, message.channel.jump_url )
            );

            embed.add_field( inline = False,
                name = "Content",
                value = message.content
            );

            await channel.send( embed=embed, allowed_mentions=False, mention_author=False );

    return HOOK_CONTINUE();

async def on_message_edit( before: discord.Message, after: discord.Message ) -> int:

    if after.author.id == bot.user.id:
        return HOOK_CONTINUE();

    if after.guild:

        channel = server_logger_channel( "message_edit", after.guild.id );

        if channel:

            embed = discord.Embed(
                color = 16711680
            );

            embed.add_field( inline = False,
                name = after.author.name,
                value = "Message sent by {} edited in {}".format( after.author.mention, after.jump_url )
            );

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
                    old_result.append(f"**{old[i1:i2]}**")
                    new_result.append(f"**{new[j1:j2]}**")
                elif tag == 'delete':
                    old_result.append(f"~~{old[i1:i2]}~~")
                elif tag == 'insert':
                    new_result.append(f"``{new[j1:j2]}``")

            old = ''
            new = ''
            for o in old_result:
                old += o;
            for n in new_result:
                new += n;

            embed.add_field( inline = False,
                name = "Before",
                value = old
            );

            embed.add_field( inline = False,
                name = "After",
                value = new
            );

            await channel.send( embed=embed, allowed_mentions=False, mention_author=False );

    return HOOK_CONTINUE();
