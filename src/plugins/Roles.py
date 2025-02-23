from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord

from src.utils.sentences import sentences
from src.utils.CCacheManager import g_Cache
from src.utils.utils import g_Utils

class CRoleSelectionView( discord.ui.View ):

    def __init__( self, roles_data: g_Cache.CCacheDictionary, placeholder: str ):

        super().__init__( timeout=None );

        options: list[discord.Role] = [];

        guild: discord.Guild = bot.get_guild( g_Utils.Guild.LimitlessPotential );

        if guild:

            for role_id, role_description in roles_data.items():

                role: discord.Role = guild.get_role( int( role_id ) );

                if g_Utils.developer:

                    options.append( discord.SelectOption( label = role_id, value = role_id, description = role_description ) );

                elif role:

                    options.append( discord.SelectOption( label = role.name, value = role_id, description = role_description ) );

            self.roles_data = roles_data;
            self.placeholder = placeholder;

            select = discord.ui.Select( placeholder = sentences[ placeholder ], options = options, custom_id = "role_select" );

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

        await interaction.message.edit( view = CRoleSelectionView( self.roles_data, self.placeholder ) );

global all_roles;
all_roles = {
    "COLORS": {
        "908115616878182400": "Red",
        "1212547281795027045": "Orange",
        "908115771664793610": "Yellow",
        "910969070977970176": "Brown",
        "908115454835441714": "Blue",
        "908115878598557768": "Purple",
        "1212548186204405811": "Pink",
        "1212548429226582036": "Grey",
        "1212547998266040380": "Light Blue",
        "908116005916659733": "Green",
        "1212548911554629722": "Lime",
        "910969284648374274": "White",
        "910969339933503489": "Black",
        "910968807261106226": "Discord's gray theme"
    },
    "CONTINENT":
    {
        "1220422733465391104": "South America",
        "1220420541496692909": "North America",
        "1220423123686653973": "Europe",
        "1220423076639150110": "Africa",
        "1220422964453838878": "Asia"
    },
    "DEVELOPER":
    {
        "1111760775736995920": "You do have knowledge of scripting languages",
        "1195977013022957618": "You do have knowledge of programing languages",
        "1111760699262251122": "You do have knowledge of 3D level design",
        "1111760858905841834": "You do have experience on 3D model design",
        "1111761018788511774": "You do have knowledge on music/audio design",
        "1111760914711068803": "You do have knowledge on 2D art design"
    },
    "PINGS":
    {
        "1311843309081067590": "Get notified when playing Garry's Mod",
        "1311843098837516288": "Get notified when playing Left 4 Dead",
        "1153074477056405624": "Get notified when playing Sven Co-op",
        "1311848524165677221": "Get notified when playing Half-Life",
        "1311863018816147497": "Get notified when playing Baldur's Gate 3",
        "1303921521969987658": "Get notified when playing Minecraft"
    },
    "OTHERS": {
        "1111484625265631262": "Your operative system is linux",
        "1288996615775981570": "Get DJ role for boogie bot",
        "1282884214244511829": "You do run a game server"
    }
}

async def role_view_setup():

    cache = g_Cache.get( "RoleManager" );

    global all_roles;

    for role_category, roles_data in all_roles.items():

        if len( roles_data ) <= 0:
            continue;

        view = CRoleSelectionView( roles_data, f"SELECT_ROLE_{role_category}" );

        channel = bot.get_channel( g_Utils.Guild.Channel_Welcome );

        message: discord.Message = None;

        if role_category in cache:

            try:

                message = await channel.fetch_message( cache[ role_category ] );

                message = await message.edit( view=view );

            except discord.NotFound:

                bot.exception( "Failed on getting CRoleSelectionView by ID. sending a new one." );

        if not message or message is None:

            message = await channel.send(view=view);

            cache[ role_category ] = message.id;
