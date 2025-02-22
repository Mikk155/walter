from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;
import datetime;

async def on_think_second( time: datetime.datetime ):

    from src.utils.utils import g_Utils;
    from src.plugins.Activity import g_Activity;

    if g_Utils.developer:
        return;

    try:

        if g_Activity.time < time:

            g_Activity.update( time );

            pActivity = discord.Activity(
                type = g_Activity.type,
                name = g_Activity.name,
                state = g_Activity.get_state(),
            );

            if pActivity:

                await bot.change_presence( activity = pActivity );

    except Exception as e:

        bot.exception( f"on_think_second: {e}" );
