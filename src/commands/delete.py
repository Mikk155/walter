from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord
from discord import app_commands;

from typing import Optional;

from src.utils.sentences import sentences
from src.utils.utils import g_Utils

@bot.tree.command()

@app_commands.guild_only()

@app_commands.default_permissions( administrator=True )

@app_commands.describe(
    amount='Amount of messages to delete by finding up in this channel',
    user='User to target messages, if none is everything',
    since='Remove messages since this message\'s id is found. "amount" is ignored if "to" is provided',
    to='If using "since" this is the message where the bot should stop, otherwise we\'ll use "amount" or stop after 5 messages.'
)

async def delete(
    interaction: discord.Interaction,
    amount: Optional[int] = None,
    user: Optional[discord.Member] = None,
    since: Optional[str] = None,
    to: Optional[str] = None,
):

    """Delete messages in a channel"""

    await interaction.response.defer( thinking=True );

    try:

        channel: discord.TextChannel = interaction.channel;

        messages = [];

        if since:

            start = await channel.fetch_message(since);

            if start:

                stop = await channel.fetch_message(to) if to else None;

                async for msg in channel.history( after=start, oldest_first=False ):

                    if stop and msg.id == stop.id:
                        break

                    if user and msg.author.id != user.id:
                        continue

                    messages.append( msg );

                    if not stop and len( messages ) >= 5:
                        break;

            else:

                await interaction.followup.send( embed=bot.m_Logger.info( "Can't find message with ID \"{}\"", since ) );

                return;

        else:

            async for msg in channel.history( limit=amount or 5 ):

                if user and msg.author.id != user.id:
                    continue;

                messages.append( msg );

        if len(messages) > 0:

            await channel.delete_messages( messages );

            embed: discord.Embed = bot.m_Logger.info( "🧹 Deleted {} message{}", len( messages ), "s" if len( messages ) > 1 else "" );

            await interaction.followup.send( embed=embed );

            channel = bot.get_channel( g_Utils.Guild.Channel_DiscordLogs );

            if channel:

                embed.add_field( name="Deleted by", value=interaction.user.global_name );

                await channel.send( embed=embed );

    except Exception as e:

        embed = bot.exception( f"command::delete: {e}", interaction );

        await interaction.followup.send( embed=embed );
