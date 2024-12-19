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
    __data__["name"] = "Role Manager";
    __data__["description"] = "Allow users to self-manage their roles";

    # Return data for g_PluginManager
    return __data__;

@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
@app_commands.describe( role='Role', description='Description', remove='True removes the role, False adds the role' )
async def cfg_roles(
    interaction: discord.Interaction,
    role: typing.Optional[discord.Role] = None,
    description: typing.Optional[str] = None,
    remove: bool = False
):
    """Configure role settings, Run w/o arguments to get the list"""

    await interaction.response.defer( thinking=True );

    try:

        cache = g_Cache.get();

        srv = cache.get( str( interaction.guild_id ), {} );

        if role:

            if remove:

                srv.pop( str( role.id ), None );

                await interaction.followup.send( f'Removed role {role.name}' );

            else:

                srv[ str( role.id ) ] = [ role.name, description if description else '' ]

                await interaction.followup.send( f'Added role {role.name}' );

            cache[ str( interaction.guild_id ) ] = srv;

        else:

            await interaction.followup.send( f'```json\n{json.dumps( srv, indent=2 )}```' );

    except Exception as e:

        await bot.exception_handle( e, interaction=interaction );

class RoleDropDown( discord.ui.Select ):

    server_id: int;

    def __init__( self, server_id, role_data ):

        self.server_id = server_id;

        options = [ discord.SelectOption( \
            label=role_data[rol][0], value=rol,
            description=role_data[rol][1] ) \
                for rol in role_data.keys()
        ];

        super().__init__( placeholder="Choose a role", min_values=1, max_values=1, options=options );

    async def callback( self, interaction: discord.Interaction ):

        try:

            choice = self.values[0];

            rol = bot.get_guild( self.server_id ).get_role( int(choice) );

            if rol in interaction.user.roles:

                await interaction.user.remove_roles( rol );

                await interaction.response.send_message( "Removed role {}".format( rol.mention ), ephemeral=True, allowed_mentions=False );

            else:

                await interaction.user.add_roles( rol );

                await interaction.response.send_message( "Added role {}".format( rol.mention ), ephemeral=True, allowed_mentions=False );

        except discord.Forbidden:

            await interaction.response.send_message( "Exception: Not enough permissions." );

        except Exception as e:

            await bot.exception_handle( e, interaction=interaction );

class CRoleView( discord.ui.View ):

    def __init__( self, server_id, role_data ):

        super().__init__();

        self.timeout = 10
        self.add_item( RoleDropDown( server_id, role_data ) );

class CRoleView( discord.ui.View ):

    def __init__( self, server_id, role_data ):

        super().__init__();

        self.add_item( RoleDropDown( server_id, role_data ) );

@bot.tree.command()
async def role( interaction: discord.Interaction ):
    """Manage your roles"""

    await interaction.response.defer( thinking=True );

    try:

        cache = g_Cache.get();

        all_roles = [];

        all_data = cache.get( str( interaction.guild_id ), {} ).copy();

        temp_data = {};

        for k, v in all_data.items():

            if interaction.guild.get_role( int(k) ):

                temp_data[k] = v;

                if len( temp_data ) >= 25:

                    all_roles.append( temp_data.copy() );

                    temp_data.clear();

        if temp_data and len(temp_data) > 0:

            all_roles.append( temp_data );

        for role_data in all_roles:

            await interaction.followup.send(
                view=CRoleView(
                    interaction.guild_id,
                    role_data
                )
            );

    except Exception as e:

        await bot.exception_handle( e, interaction=interaction );
