from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord
from discord import app_commands;

from typing import Optional;

from src.utils.utils import g_Utils;

async def get_message_id_url( message:str, channel: discord.TextChannel ) -> discord.TextChannel | None:

    fetch_message: discord.Message = None;

    # Find by url
    if message.find( 'https://' ) != -1:

        async for msg in channel.history():

            if msg and msg.jump_url == message:

                fetch_message = msg;

                break;

    else:

        fetch_message = await channel.fetch_message( message );

    return fetch_message;

@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions( administrator=True )
@app_commands.describe(
    message='ID or url of the message to delete',
    reason='Reason'
)
async def delete_single( interaction: discord.Interaction, message: str, reason: Optional[str] = None ):
    '''Delete a single message by ID or url'''

    await interaction.response.defer( thinking=True, ephemeral=True );

    try:

        channel: discord.TextChannel = interaction.channel;

        fetch_message: discord.Message = get_message_id_url( message, channel );

        if fetch_message:

            from src.plugins.delete_log import delete_notice;

            await delete_notice( fetch_message, interaction.user.id );

            embed: discord.Embed = discord.Embed(
                color = 0xFF0000
            );

            embed.add_field( inline = False,
                name = fetch_message.author.name,
                value = f"🧹 Deleted message by <@{interaction.user.id}>"
            );

            if reason:

                embed.add_field( inline = False, name='Reason', value=reason );

            await fetch_message.reply( embed=embed );

            await fetch_message.delete();

            await interaction.followup.send( embed=embed, ephemeral=True );

        else:

            await interaction.followup.send( embed=bot.m_Logger.info( "couldn't find the message in this channel " ) );

    except Exception as e:

        embed = bot.exception( f"command::delete_single: {e}", interaction );

        await interaction.followup.send( embed=embed );


# async def delete(
#     interaction: discord.Interaction,
#     amount: Optional[int] = None,
#     user: Optional[discord.Member] = None,
#     since: Optional[str] = None,
#     to: Optional[str] = None,
# ):

#     """Delete messages in a channel"""

#     await interaction.response.defer( thinking=True, ephemeral=True );

#     try:

#         channel: discord.TextChannel = interaction.channel;

#         messages = [];

#         if since:

#             start = await channel.fetch_message(since);

#             if start:

#                 stop = await channel.fetch_message(to) if to else None;

#                 async for msg in channel.history( after=start, oldest_first=False ):

#                     if stop and msg.id == stop.id:
#                         break

#                     if user and msg.author.id != user.id:
#                         continue

#                     messages.append( msg );

#                     if not stop and len( messages ) >= 5:
#                         break;

#             else:

#                 await interaction.followup.send( embed=bot.m_Logger.info( "Can't find message with ID \"{}\"", since ) );

#                 return;

#         else:

#             async for msg in channel.history( limit=amount or 5 ):

#                 if user and msg.author.id != user.id:
#                     continue;

#                 messages.append( msg );

#         if len(messages) > 0:

#             await channel.delete_messages( messages );

#             embed: discord.Embed = bot.m_Logger.info( "🧹 Deleted {} message{}", len( messages ), "s" if len( messages ) > 1 else "" );

#             await interaction.followup.send( embed=embed );

#             channel = bot.get_channel( g_Utils.Guild.Channel_DiscordLogs );

#             if channel:

#                 embed.add_field( name="Deleted by", value=interaction.user.global_name );

#                 await channel.send( embed=embed );

#     except Exception as e:

#         embed = bot.exception( f"command::delete: {e}", interaction );

#         await interaction.followup.send( embed=embed );
