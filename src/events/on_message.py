'''
    Event called when a member sends a message
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import re;
import pytz;
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

                all_words = message.content.split( " " );

                for word in all_words:

                    word_times = 0;

                    if word in used_words:

                        word_times = used_words[ word ];

                    word_times = word_times + 1;

                    used_words[ word ] = word_times;

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

                        from src.utils.utils import g_Utils;

                        g_Cache.set_temporal( "control_arase_mimido", datetime.timedelta( hours = ( 6 - hour ) ) );

                        user = await bot.fetch_user( 438449162527440896 );

                        webhook = await bot.webhook( message.channel );

                        await webhook.send( content='[What the fuck arase go to sleep](https://cdn.discordapp.com/attachments/342709269017133064/1292115993040126083/SPOILER_youtube-jDgMkHB1pEI.mp4?ex=6702904b&is=67013ecb&hm=816913c613de3cd284f7765b3d13383b1251ee35bf62eee4d953c30c2cc004bb&)', username='KEZÆIV', avatar_url=user.avatar.url if user.avatar else None );

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
