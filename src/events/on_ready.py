'''
    Event called when the bot is run for the first time.
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

@bot.event
async def on_ready() -> None:

    print( f"Bot connected and logged as {bot.user.name}#{bot.user.discriminator}" );

    await bot.wait_until_ready();

    try:

        from src.events.on_think import on_think;

        if not on_think.is_running():
        #
            on_think.start();
        #

    except Exception as e:

        bot.exception( f"on_ready: {e}" );
