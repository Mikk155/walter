from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

@bot.event
@bot.exception
async def on_guild_emojis_update( guild: discord.Guild, before: list[discord.Emoji], after: list[discord.Emoji] ) -> None:
#
    pass;
#
