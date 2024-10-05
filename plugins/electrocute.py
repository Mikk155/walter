from plugins.main import *

@bot.tree.command()
@app_commands.describe(
    member='Member',
)
async def electrocute( interaction: discord.Interaction, member: discord.Member ):
    """Electrocute a member and sent him to sleep"""

    try:
        await interaction.response.send_message( '{} Sent {} to sleep [media]({})'.format( interaction.user.mention, member.mention, "https://cdn.discordapp.com/attachments/342709269017133064/1292115993040126083/SPOILER_youtube-jDgMkHB1pEI.mp4?ex=6702904b&is=67013ecb&hm=816913c613de3cd284f7765b3d13383b1251ee35bf62eee4d953c30c2cc004bb&" ) )
    except Exception as e:
        await interaction.response.send_message( "Exception: {}".format( e ), ephemeral=True );
