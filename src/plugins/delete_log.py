'''
    Call to notice if a message has been deleted
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;
from typing import Optional

async def delete_notice( message: discord.Message, deleter_id: Optional[int] = None ):

    from src.utils.utils import g_Utils;

    if not message.guild or message.guild.id != g_Utils.Guild.LimitlessPotential or message.id in bot.deleted_messages:

        return;

    channel = bot.get_channel( g_Utils.Guild.Channel_DiscordLogs );

    if not channel:

        return;

    embed = discord.Embed(
        color = 0xFF0000
    );

    embed.add_field( inline = False,
        name = message.author.name,
        value = "Message sent by {} deleted in {}".format( message.author.mention, message.channel.jump_url )
    );

    if message.content:

        content = message.content;

        if len(content) > 1024:

            part = 1;

            while len( content ) > 1024:

                content_part = content[ : 1024 ];
                content = content[ 1024 : ];

                embed.add_field( inline = False,
                    name = f"Content split {part}",
                    value = content_part
                );

                part = part + 1;

            if len(content) > 0:

                embed.add_field( inline = False,
                    name = "Content",
                    value = content
                );

        else:

            embed.add_field( inline = False,
                name = "Content",
                value = content
            );

    if deleter_id:

        embed.add_field( inline = False,
            name = "Deleted by",
            value = f"<@{deleter_id}>"
        );

    else:

        async for entry in message.guild.audit_logs(limit=5, action=discord.AuditLogAction.message_delete):
            if entry.target.id == message.author.id:
                embed.add_field( inline = False,
                    name = "Deleted by",
                    value = f"<@{entry.user_id}>"
                );
                break;

    if message.embeds and len(message.embeds) > 0:

        embeds = message.embeds;

        embeds.insert( 0, embed );

        await channel.send( embeds=embeds, allowed_mentions=False, mention_author=False, silent=True );

    else:

        await channel.send( embed=embed, allowed_mentions=False, mention_author=False, silent=True );
