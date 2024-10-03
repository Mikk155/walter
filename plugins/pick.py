
from plugins.main import *

@bot.tree.command()
@app_commands.describe(
    options='Separate options by using comas',
)
async def pick( interaction: discord.Interaction, options: str ):
    """Make the bot decide a option for you"""
    try:
        items = options.split( ',' );
        if len( items ) > 1:
            option = str( items[ random.randint( 0, len( items ) - 1 ) ] );
            await interaction.response.send_message( "From ``{}``\nI choose.... ``{}``".format( options, option.strip( " " ) ) );
        else:
            await interaction.response.send_message( "You have to provide at least two options", ephemeral=True );
    except Exception as e:
        await interaction.response.send_message( "Exception: {}".format( e ), ephemeral=True );
