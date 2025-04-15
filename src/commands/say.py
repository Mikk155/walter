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

#@app_commands.default_permissions( administrator=True )

@app_commands.describe(
    message='Say something',
    user='User to use identity',
    file='File to upload'
)

async def say(
    interaction: discord.Interaction,
    message: Optional[str] = None,
    user: Optional[discord.Member] = None,
    file: Optional[discord.Attachment] = None
):

    """Make the bot say something"""

    await interaction.response.defer( thinking=True, ephemeral=True );

    try:

        if not user:

            user = bot.user;

        webhook = await bot.webhook( interaction.channel );

        avatar = user.avatar.url if user.avatar else None;

        if file:
            file_send = await file.to_file();
            said: discord.WebhookMessage = await webhook.send( content=message, username=user.display_name, file=file_send, avatar_url=avatar, wait=True );
        else:
            said: discord.WebhookMessage = await webhook.send( content=message, username=user.display_name, avatar_url=avatar, wait=True );

        channel = bot.get_channel( g_Utils.Guild.Channel_DiscordLogs );

        if channel:

            await channel.send( embed = bot.m_Logger.info( sentences[ "SAY_MEMBER_SAID" ], interaction.user.global_name, said.jump_url, message ), silent=True );

        await interaction.delete_original_response();

    except Exception as e:

        embed = bot.exception( f"command::say: {e}", interaction );

        await interaction.followup.send( embed=embed );
