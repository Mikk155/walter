'''
    Event called when a member sends a message
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import re;
import pytz;
import random;
import discord;
import datetime;

from typing import Optional

async def on_message( message: discord.Message ):

    from src.utils.CCacheManager import g_Cache;
    from src.utils.utils import g_Utils

    try:

        content_lower = message.content.lower();

        if message.guild and message.guild.id == g_Utils.Guild.LimitlessPotential:

#            from src.plugins.EmojiManager import check_emoji;
#            check_emoji(message);

            if message.content and not message.author.bot:

                used_words = g_Cache.get( "most_used_word" );

                all_words = message.content.lower().split( " " );

                COMMON_WORDS = (
                    "the", "and", "you", "that", "for", "but", "with", "just", "like", "have",
                    "a", "an", "to", "in", "of", "on", "at", "is", "it", "this", "i", "we",
                    "they", "he", "she", "him", "her", "was", "were", "be", "been", "am",
                    "are", "as", "by", "not", "do", "does", "did", "so", "if", "or", "from",
                    "my", "your", "our", "their", "them", "me", "us", "can", "could", "should",
                    "would", "will", "shall", "there", "what", "which", "who", "whom", "how",
                    "when", "where", "why", "because", "about", "into", "up", "down", "out",
                    "over", "under", "again", "then", "than", "too", "very", "no", "yes",
                    "also", "more", "most", "some", "such", "each", "few", "many", "every",
                    "any", "all", "these", "those"
                );

                for word in all_words:

                    if not word or len(word) < 3 or word in COMMON_WORDS or word.startswith( '<:' ):
                        continue;

                    word_times = 0;

                    if word in used_words:

                        word_times = used_words[ word ];

                    word_times = word_times + 1;

                    used_words[ word ] = word_times;

            if message.channel.id == g_Utils.Guild.Channel_LPMemes and message.author.id != bot.user.id:

                Elements = len(message.embeds) + len(message.attachments);

                if Elements == 0 and not message.author.guild_permissions.administrator:

                    response = await message.reply( f"This channel is for memes only. Please forward your target message and reply somewhere else",\
                                            silent=True, delete_after=10 );

                    bot.deleted_messages.append( response.id );

                    await message.delete();

                    return;

            # Remove sent messages to #welcome #-TODO Should we use a button + vgui instead of a app command
            if message.channel.id == g_Utils.Guild.Channel_Welcome and not message.author.guild_permissions.administrator:

                await message.delete();

                return

            # Count together channel
            elif message.channel.id == g_Utils.Guild.Channel_CountTogether and not message.author.bot:

                async def count_wrong( msg: discord.Message, number: Optional[int] = None ):

                    if msg:

                        if number:

                            response = await msg.reply( f"Expected {number}", silent=True, delete_after=10 );

                            bot.deleted_messages.append( response.id );

                        try:

                            await msg.add_reaction( '❌' );

                        except:

                            await msg.delete();

                cache = g_Cache.get( "count_together" );

                if "number" in cache:

                    num = re.search( r'\b(\d+)\b', message.content );

                    if num:

                        current = int( num.group(1) );

                        desired = cache.get( "number", 0 ) + 1;

                        if desired != current:

                            await count_wrong( message, desired );

                        else:

                            cache[ "number" ] = desired;

                    else:

                        await count_wrong( message );

            # Control arase
            if message.author.id in [ 768337526888726548, 1312014737449549826 ]:

                if not g_Cache.has_temporal( "control_arase_mimido" ):

                    hour = datetime.datetime.now( pytz.timezone( "Asia/Kuala_Lumpur" ) ).hour;

                    if hour <= 5:

                        if message.content.find( "test" ) != -1 and random.randint( 0, 1 ) == 1:

                            from src.utils.utils import g_Utils;

                            g_Cache.set_temporal( "control_arase_mimido", datetime.timedelta( hours = ( 6 - hour ) ) );

                            user = await bot.fetch_user( 438449162527440896 );

                            webhook = await bot.webhook( message.channel );

                            mimir_texts = [
                                "What the fuck arase go to sleep",
                                "Go to fucking sleep arase",
                                "Ok but go to sleep",
                                "when sleeping",
                                "Mimir time mf",
                                "You ain't going to find a girlfriend at this time,"
                                f"Reminder para <@{message.author.id}> to fucking sleep early"
                            ];

                            if hour == 0:
                                hour = f' It\'s 12 PM.';
                            else:
                                hour = f' It\'s {hour} AM.';

                            mimir_text = mimir_texts[ random.randint( 0, len(mimir_texts) - 1 ) ] + hour;

                            await webhook.send( content=f'{mimir_text} [a mimir](https://cdn.discordapp.com/attachments/847485688282480640/1376229990378508398/a_mimir.mp4?ex=6834918e&is=6833400e&hm=ea97d291d22f7a0dbc723032baee9ce6d4e195e112913df24b786cfb9e697e2a&)', username='KEZÆIV', avatar_url=user.avatar.url if user.avatar else None );

                if not g_Cache.has_temporal( "control_arase_horny" ):

                    arase_words = [
                        'mommy',
                        'mama',
                        'sex',
                        'gf',
                        'feet',
                        'armpit'
                    ];

                    for h in arase_words:

                        if h in content_lower:

                            user = await bot.fetch_user( 121735805369581570 );

                            cache = g_Cache.get( "control_arase" );

                            number = cache.get( "times", 0 );

                            number += 1;

                            cache[ "times" ] = number;

                            webhook = await bot.webhook( message.channel );

                            await webhook.send( content=f'Control yourself. This is the {number}th time.', username='KernCore', avatar_url=user.avatar.url if user.avatar else None );

                            g_Cache.set_temporal( "control_arase_horny", datetime.timedelta( hours = 1 ) );

                            return;

            # Neko marry sara
            elif message.author.id == g_Utils.Guild.Owner:

                if 'neko marry' in content_lower:

                    sare: discord.User = bot.get_guild( g_Utils.Guild.LimitlessPotential ).get_member( 746914044828450856 );

                    if sare and sare in message.mentions:

                        cache = g_Cache.get( "marry_sare" );

                        number = cache.get( "times", 52 );

                        number += 1;

                        await bot.get_channel( message.channel.id ).send( f"Mikk has confesed his love to Sare {number} times.", mention_author=False );

                        cache[ "times" ] = number;

        if 'woman moment' in content_lower or 'woman unmoment' in content_lower:

            bunnt: discord.User = bot.get_guild( g_Utils.Guild.LimitlessPotential ).get_member( 740196277844967458 );

            if bunnt:

                cache = g_Cache.get( "woman_moment" );

                number = cache.get( "moment", 0 );

                number = ( number + 1 ) if 'woman moment' in content_lower else ( number - 1 );

                nombre_actual = bunnt.display_name;

                moment = re.sub( r'\d+', str(number), nombre_actual );

                if not str(number) in moment:

                    moment = '{} {}'.format( moment, number );

                await bunnt.edit( nick=moment);

                cache[ "moment" ] = number;

    except Exception as e:

        bot.exception( f"on_message: {e}" );
