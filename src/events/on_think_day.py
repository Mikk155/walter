from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import random
import discord;
import datetime;

async def on_think_day( time: datetime.datetime ):

    from src.utils.utils import g_Utils;
    from src.utils.CCacheManager import g_Cache;

    try:

        if time.isoweekday() == 7:

            channel = bot.get_channel( 1343196084876476499 );

            if channel:

                used_words = g_Cache.get( "most_used_word" );
                items = list(used_words.items());

                random.shuffle( items );

                items.sort( key=lambda item: item[1], reverse=True );

                most_used = [ key for key, value in items ];

                how_many = 0;

                embed = discord.Embed( color = discord.Color(0xda00ff), title="Weekly words", \
                    description = "Top most used words this week" )

                for word in most_used:

                    if how_many >= 10:
                        break;

                    how_many = how_many + 1;

                    word_times = used_words[ word ];

                    embed.add_field( inline = False, name = word, \
                                    value = f"Used {word_times} times this week" );

                await channel.send( embed=embed );
            
                used_words.clear();

#        from src.plugins.EmojiManager import manage_emojis;
#        await manage_emojis();

        birthdays = g_Cache.get( "birthdays" );

        off_topic_channel = bot.get_channel( 1343196084876476499 );

        for user, data in birthdays.items():

            if data[0] == time.day and data[1] == time.month and off_topic_channel:

                await off_topic_channel.send( f"Everyone give <@{user}> a happy birthday! <:kaleun:1212181960890253372>🎉" );

    except Exception as e:

        bot.exception( f"on_think_day: {e}" );
