from plugins.main import *

@bot.tree.command()
@app_commands.describe(
    message='Say something',
#    reply='Message link to reply',
    hidename='Hide who used the command, Only works for administrators',
)
async def pick( interaction: discord.Interaction, message: str, hidename: bool = True ):
    """Make the bot say something"""
    try:
        if hidename and interaction.user.guild_permissions.administrator:
            await interaction.channel.send( message );
        else:
            await interaction.response.send_message( message );
    except Exception as e:
        await interaction.response.send_message( "Exception: {}".format( e ), ephemeral=True );

        await message.channel.send( "You have to specify a text" );
