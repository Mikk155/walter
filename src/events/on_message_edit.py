'''
    Event called when a member edits a message
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import difflib
import discord;

@bot.event
async def on_message_edit( before: discord.Message, after: discord.Message ):

    from src.utils.utils import g_Utils

    try:

        if after.guild:

            if after.guild.id == g_Utils.Guild.LimitlessPotential:

                channel = bot.get_channel( g_Utils.Guild.Channel_DiscordLogs );

                if channel and after.author.id != bot.user.id:

                    embed = discord.Embed(
                        color = 0x00FF00
                    );

                    embed.add_field( inline = False,
                        name = after.author.name,
                        value = "Message sent by {} edited in {}".format( after.author.mention, after.jump_url )
                    );

                    old = before.content;
                    new = after.content;

                    matcher = difflib.SequenceMatcher( None, old, new )
                    old_result = []
                    new_result = []

                    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
                        if tag == 'equal':
                            old_result.append(old[i1:i2])
                            new_result.append(new[j1:j2])
                        elif tag == 'replace':
                            old_result.append(f"**{old[i1:i2]}**")
                            new_result.append(f"**{new[j1:j2]}**")
                        elif tag == 'delete':
                            old_result.append(f"~~{old[i1:i2]}~~")
                        elif tag == 'insert':
                            new_result.append(f"``{new[j1:j2]}``")

                    old = ''
                    new = ''
                    for o in old_result:
                        old += o;
                    for n in new_result:
                        new += n;

                    if old != new:

                        embed.add_field( inline = False,
                            name = "Before",
                            value = old
                        );

                        embed.add_field( inline = False,
                            name = "After",
                            value = new
                        );

                        await channel.send( embed=embed, allowed_mentions=False, mention_author=False );

    except Exception as e:

        bot.exception( f"on_message_edit: {e}", after );
