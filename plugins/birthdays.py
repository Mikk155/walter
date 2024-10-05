from plugins.main import *

hooks = [
    Hooks.on_ready
];

RegisterHooks( __file__, hook_list=hooks );

async def on_ready():

    birthdays = jsonc( '{}\\plugins\\birthdays.json'.format( abspath ) );

    date = datetime.now()

    for user, birthday in birthdays.items():
        if birthday[0] == date.month and birthday[1] == date.day:
            try:
                await bot.get_channel( birthday[2] ).send( "Everyone wish a Happy Birthday to {}".format( user ) );
            except Exception as e:
                pass

@bot.tree.command()
@app_commands.describe(
    month='month',
    day='day',
    user='Member to set (Administrators only)',
)
@app_commands.choices( month=MONTH_CHOICES )
async def birthday( interaction: discord.Interaction, month: app_commands.Choice[str], day: int, user: Optional[discord.Member] = None ):
    """Set your birthday"""

    try:

        if user is None:
            user = interaction.user;
        else:
            if user != interaction.user and not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message( "Only administrators can set other's birthday", ephemeral=True );
                return;

        mention = user.mention;

        if mention.find( '!' ) != -1:
            mention = mention.replace( '!', '' );

        birthdays = jsonc( '{}\\plugins\\birthdays.json'.format( abspath ) );
        birthdays[ mention ] = [ int(month.value), day, interaction.channel_id ];
        open( '{}\\plugins\\birthdays.json'.format( abspath ), 'w' ).write( json.dumps( birthdays, indent = 0 ) );
        await interaction.response.send_message( "The user {} birthday has been set {}/{}".format( mention, month.value, day ) )

    except Exception as e:

        await interaction.response.send_message( f"Exception {e}", ephemeral=True );
