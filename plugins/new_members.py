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
    __data__["name"] = "New members";
    __data__["description"] = "Track new members";
    __data__["hooks"] = [ Hooks.on_member_join, Hooks.on_message ];

    return __data__;

@bot.tree.command( guild=bot.get_guild( 1118352656096829530 ) )
@app_commands.guild_only()
@app_commands.describe(
    why='Why you joined this server?'
)
async def verify( interaction: discord.Interaction, why: str ):
    """Ask for a verification"""

    await interaction.response.defer( ephemeral=True, thinking=True );

    try:

        if interaction.channel_id != 1118352656096829530 \
        or not interaction.guild.get_role( 1316214066384994324 ) in interaction.user.roles:

            return;

        if why:

            admin = await bot.get_channel( 1287940238202769418 ).send(
                    embed=discord.Embed(
                    title = f"User {interaction.user.name} used verification",
                    description = f"{interaction.user.mention} Response: {why} <@438449162527440896>",
                    color = 16711680
                )
            );

            try:
                await admin.pin();
            except:
                pass

        await interaction.followup.send( "An administrator will confirm your identity.\nThis will take some time.\nWe apologize for the inconveniences.", ephemeral=True );

    except Exception as e:

        await bot.exception_handle( e, interaction=interaction );

async def on_member_join( member : discord.Member ) -> int:

    member.add_roles( member.guild.get_role( 1316214066384994324 ) );

async def on_message( message: discord.Message ) -> int:

    if message.channel.id == 1118352656096829530 and not message.author.guild_permissions.administrator:

        await message.delete();

    return HOOK_CONTINUE();
