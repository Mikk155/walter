from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;
import datetime;

async def on_think_day( time: datetime.datetime ):

    from src.utils.utils import g_Utils;
    from src.utils.CCacheManager import g_Cache;

    try:

#        from src.plugins.EmojiManager import manage_emojis;
#        await manage_emojis();

        birthdays = g_Cache.get( "birthdays" );

        off_topic_channel = bot.get_channel( 1343196084876476499 );

        for user, data in birthdays.items():

            if data[0] == time.day and data[1] == time.month and off_topic_channel:

                await off_topic_channel.send( f"Everyone give <@{user}> a happy birthday! <:kaleun:1212181960890253372>🎉" );

    except Exception as e:

        bot.exception( f"on_think_day: {e}" );
