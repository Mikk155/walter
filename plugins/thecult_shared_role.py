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

global TheCultSharedRole;
class TheCultSharedRole:

    LP = 744769532513615922;
    TC = 1216162825307820042;

    def iterate( member_id: int, server_id: int ) -> bool:
        return bot.get_guild( server_id ).get_member( member_id );

    def check( member_id: int, server_id: int, server_id2: int ) -> bool:
        return ( bot.get_guild( server_id ).get_member( member_id ) and bot.get_guild( server_id2 ).get_member( member_id ));

async def manage_role( member_id: int, ShouldAdd: bool = False ):

    rol = discord.utils.get( bot.get_guild( TheCultSharedRole.LP ).roles, name="The Cult Member" );

    member = bot.get_guild( TheCultSharedRole.LP ).get_member( member_id );

    if not member:
        return;

    if ShouldAdd:

        if not rol in member.roles:

            await member.add_roles( rol );

            await bot.get_channel( 842174687445778483 ).send( f'{member.mention} is now a cult member <:elegant:1216204366349078631>\n' );

    elif rol in member.roles:

        await member.remove_roles( rol );

async def on_ready():

    # Iterate through The cult as it have less members
    for miembro in bot.get_guild( TheCultSharedRole.TC ).members:

        await manage_role( miembro.id, TheCultSharedRole.iterate( miembro.id, TheCultSharedRole.LP ) );

    return Hook.Continue();

async def on_member_join( member : discord.Member ):

    await manage_role( member.id, TheCultSharedRole.check( member.id, TheCultSharedRole.LP, TheCultSharedRole.TC ) );

    return Hook.Continue();

async def on_member_remove( member : discord.Member ):

    await manage_role( member.id, TheCultSharedRole.check( member.id, TheCultSharedRole.LP, TheCultSharedRole.TC ) );

    return Hook.Continue();
