from plugins.main import *

@bot.tree.command()
@app_commands.describe(
    message='Say something',
#    reply='Message link to reply',
    hidename='Hide who used the command, Only works for administrators',
)
async def say( interaction: discord.Interaction, message: str, hidename: bool = True ):
    """Make the bot say something"""

    try:
        if hidename and interaction.user.guild_permissions.administrator:
            await interaction.response.send_message( '<:walter_what:1278078147870331011>', ephemeral=True, delete_after=0.1 )
            await interaction.channel.send( message );
        else:
            await interaction.response.send_message( message );
    except Exception as e:
        await interaction.response.send_message( "Exception: {}".format( e ), ephemeral=True );
