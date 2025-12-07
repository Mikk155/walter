from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;
from datetime import timedelta;
from typing import Optional;
from src.const import Colors, LimitlessPotential, TheCult;
from discord import app_commands;

@bot.tree.command()
@app_commands.guild_only()
@app_commands.describe(
    user='Member',
    days='days',
    hours='hours',
    minutes='minutes',
    seconds='seconds',
    reason='reason'
)
@bot.exception
async def timeout(
    interaction: discord.Interaction,
    user: discord.Member,
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
    reason: Optional[str] = None
) -> None:
#
    """Timeout a member"""

    if not interaction.user.guild_permissions.mute_members:
    #
        await interaction.response.send_message( "You can't use this command.\nmissing permisions ``mute_members``\nThis issue will be reported :pensive:" );
        return;
    #

    if minutes + days + seconds + hours == 0:
    #
        await interaction.response.send_message( "You have to specify an amount of time.", ephemeral=True );
        return;
    #

    time = "";

    if days > 0:
        time += f'{days}d ';
    if hours > 0:
        time += f'{hours}h ';
    if minutes > 0:
        time += f'{minutes}m ';
    if seconds > 0:
        time += f'{seconds}s ';

    if not reason:
    #
        reason = "Not specified.";
    #

    delta = timedelta( minutes=minutes, days=days, seconds=seconds, hours=hours );

    await user.timeout( delta, reason=reason );

    embed = discord.Embed(
        title = "Time out",
        description = f"<@{user.id}> was muted by <@{interaction.user.id}>\nDuration: {time}\nReason: {reason}",
        color = Colors.Orange
    );

    await interaction.response.send_message( embed=embed );

    logChannel: discord.TextChannel = None;

    if interaction.guild.id == LimitlessPotential.id:
    #
        logChannel = bot.get_channel( LimitlessPotential.Channels.DiscordLogs );
    #
    elif interaction.guild.id == TheCult.id:
    #
        logChannel = bot.get_channel( TheCult.Channels.DiscordLogs );
    #

    if logChannel:
    #
        await logChannel.send( embed = embed, allowed_mentions = False, silent = True );
    #
#
