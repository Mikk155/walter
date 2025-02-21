'''
    Event called when a member deletes a message
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

from src.utils.constants import guild_limitlesspotential_id

@bot.event
async def on_message_delete( message: discord.Message ):

    try:

        if message.guild and message.guild.id == guild_limitlesspotential_id():

            if not message.id in bot.deleted_messages and message.author.id != bot.user.id:

                channel = bot.get_channel( 877268843330961499 );

                if channel:

                    embed = discord.Embed(
                        color = 0xFF0000
                    );

                    embed.add_field( inline = False,
                        name = message.author.name,
                        value = "Message sent by {} deleted in {}".format( message.author.mention, message.channel.jump_url )
                    );

                    embed.add_field( inline = False,
                        name = "Content",
                        value = message.content
                    );

                    if message.embeds and len(message.embeds) > 0:

                        embeds = message.embeds;

                        embeds.insert( 0, embed );

                        await channel.send( embeds=embeds, allowed_mentions=False, mention_author=False, silent=True );

                    else:

                        await channel.send( embed=embed, allowed_mentions=False, mention_author=False, silent=True );

    except Exception as e:

        bot.exception( f"on_message_delete: {e}", message );
