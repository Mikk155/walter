'''
    Events called when the bot thinks
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

from src.utils.utils import g_Utils;
from src.utils.CCacheManager import g_Cache;

from src.plugins.Activity import g_Activity;

async def on_think_second():

    try:

        now = g_Utils.time();

        if g_Activity.time < now:

            g_Activity.update( now );

            pActivity = discord.Activity(
                type = g_Activity.type,
                name = g_Activity.name,
                state = g_Activity.get_state(),
            );

            if pActivity:

                await bot.change_presence( activity = pActivity );

    except Exception as e:

        bot.exception( f"on_think_second: {e}" );

async def on_think_minute():

    try:

        ''''''

    except Exception as e:

        bot.exception( f"on_think_minute: {e}" );

async def on_think_hour():

    try:

        ''''''

    except Exception as e:

        bot.exception( f"on_think_hour: {e}" );

async def on_think_day():

    try:

        ''''''

    except Exception as e:

        bot.exception( f"on_think_day: {e}" );
