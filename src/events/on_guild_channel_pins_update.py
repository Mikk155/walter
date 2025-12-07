from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;
from datetime import datetime;

@bot.event
@bot.exception
async def on_guild_channel_pins_update( channel: discord.TextChannel | discord.Thread, last_pin: datetime ) -> None:
#
    pass;
#
