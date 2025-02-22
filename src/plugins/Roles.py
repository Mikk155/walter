from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord

from src.utils.sentences import sentences
from src.utils.CCacheManager import g_Cache
from src.utils.utils import g_Utils

class CRoleSelectionView( discord.ui.View ):

    def __init__( self, roles_data: g_Cache.CCacheDictionary ):

        super().__init__( timeout=None );

        options: list[discord.Role] = [];

        guild: discord.Guild = bot.get_guild( g_Utils.Guild.LimitlessPotential );

        if guild:

            for role_id, role_description in roles_data.items():

                role: discord.Role = guild.get_role( int( role_id ) );

                if role:

                    options.append( discord.SelectOption( label = role.name, value = role_id, description = role_description ) );

            self.roles_data = roles_data;

            select = discord.ui.Select( placeholder = sentences[ "SELECT_ROLE" ], options = options, custom_id = "role_select" );

            select.callback = self.select_role;

            self.add_item( select );

    async def select_role(self, interaction: discord.Interaction):

        try:

            role = interaction.guild.get_role( int( interaction.data[ "values" ][0] ) )

            if role in interaction.user.roles:

                await interaction.user.remove_roles( role );

                await interaction.response.send_message( sentences[ "ROLE_REMOVED" ].format( role.name ), ephemeral=True );

            else:

                await interaction.user.add_roles( role );

                await interaction.response.send_message( sentences[ "ROLE_ADDED" ].format( role.name ), ephemeral=True );

        except Exception as e:

            bot.exception( f"CRoleSelectionView::select_role: {e}" );

        await interaction.message.edit( view = CRoleSelectionView( self.roles_data ) );

async def role_view_setup():

    cache = g_Cache.get( "RoleManager" );

    if "roles" in cache:

        roles_data = cache[ "roles" ]

        if len( roles_data ) <= 0:
            return;

        view = CRoleSelectionView( roles_data );

        channel = bot.get_channel( g_Utils.Guild.Channel_Welcome );

        message: discord.Message = None;

        if "menu_id" in cache:

            try:

                message = await channel.fetch_message( cache[ "menu_id" ] );

                message = await message.edit( view=view );

            except discord.NotFound:

                bot.exception( "Failed on getting CRoleSelectionView by ID. sending a new one." );

        if not message or message is None:

            message = await channel.send(view=view);

            cache[ "menu_id" ] = message.id;
