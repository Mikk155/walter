
from plugins.main import *

hooks = [
    Hooks.on_member_join,
    Hooks.on_ready
];

RegisterHooks( __file__, hook_list=hooks );

async def set_role( member: discord.Member ):

    if member:

        rol = discord.utils.get( bot.get_guild( 744769532513615922 ).roles, name="The Cult Member" )

        if not rol in member.roles:

            await member.add_roles( rol )

            await bot.get_channel( 842174687445778483 ).send( f'{member.mention} is now a cult member <:elegant:1216204366349078631>\n' )

async def on_ready():

    for miembro in bot.get_guild( 1216162825307820042 ).members:

        member = bot.get_guild( 744769532513615922 ).get_member( miembro.id )

        if member:

            await set_role( member )

async def on_member_join( member : discord.Member ):

    tcm = bot.get_guild( 1216162825307820042 ).get_member( member.id )

    lpm = bot.get_guild( 744769532513615922 ).get_member( member.id )

    if tcm and lpm:

        await set_role( lpm )
