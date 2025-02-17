from __main__ import bot
from src.Bot import Bot
bot: Bot

import discord

@bot.tree.command( guild=bot.get_guild( 744769532513615922 ) )
@discord.app_commands.guild_only()
@discord.app_commands.describe(
    why='Why you joined this server?'
)
async def verify( interaction: discord.Interaction, why: str ):
    """Ask for a verification"""

    await interaction.response.defer( ephemeral=True, thinking=True );

    try:

        if interaction.channel_id != 1118352656096829530 \
        or not interaction.guild.get_role( 1316214066384994324 ) in interaction.user.roles:

            return;

        admin = await bot.get_channel( 1287940238202769418 ).send(
                embed=discord.Embed(
                title = f"User {interaction.user.name} used verification",
                description = f"{interaction.user.mention} Response: {why}",
                color = 16711680
            )
        );

        await interaction.followup.send( "An administrator will confirm your identity.\nThis will take some time.\nWe apologize for the inconveniences.", ephemeral=True );

    except Exception as e:

        embed = bot.exception( e )

        await interaction.followup.send( ephemeral=True, embed=embed )
