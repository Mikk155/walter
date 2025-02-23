from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;
import datetime;

global active_channels;
active_channels: list[int] = [
    846124305329815632 # copybind
];

async def on_think_day( time: datetime.datetime ):

    from src.utils.utils import g_Utils;
    from src.plugins.Activity import g_Activity;

    try:

        ''''''

    except Exception as e:

        bot.exception( f"on_think_day: {e}" );
