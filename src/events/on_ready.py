from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

@bot.event
@bot.exception
async def on_ready() -> None:

    print( f"Bot connected and logged as {bot.user.name}#{bot.user.discriminator}" );

    await bot.wait_until_ready();

    if bot.__Started__ is False: # This is the first time the bot is running. since on_ready is called multiple times
    #
        bot.__Started__ = True;
    #
    else: # Otherwise this is called from a connection recovered
    #
        pass;
    #

    from src.events.on_think import on_think;
    if not on_think.is_running():
    #
        on_think.start();
    #
