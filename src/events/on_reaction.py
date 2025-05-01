'''
    Event called when a member adds/removes a reaction
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

class ReactionAction:
    removed = 0;
    added = 1;

async def on_reaction( reaction: discord.Reaction, user : discord.User, action: ReactionAction ):

    from src.utils.utils import g_Utils

    try:
        ''''''
#        if reaction.message.guild and reaction.message.guild.id == g_Utils.Guild.LimitlessPotential:

#            if action == ReactionAction.added:

#                from src.plugins.EmojiManager import check_emoji;
#                check_emoji(reaction);

    except Exception as e:

        bot.exception( f"on_message_edit: {e}" );
