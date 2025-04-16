from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

from src.utils.CCacheManager import g_Cache;
from src.utils.utils import g_Utils;
from src.utils.fmt import fmt

import os
import aiohttp
import discord
import random

def check_emoji( input: discord.Reaction | discord.Message ) -> None:

    ename: str = None;

    emoji_text = input.emoji if isinstance( input, discord.Reaction ) else input.content;

    if not isinstance( emoji_text, str ):
        emoji_text = str(emoji_text);

    has_emoji = emoji_text.find( "<:" );

    if has_emoji != -1:

        emoji_text = emoji_text[ has_emoji + 2 : ];

        ename = emoji_text[ : emoji_text.find( ":", has_emoji ) ];

    if ename:

        guild = bot.get_guild( g_Utils.Guild.LimitlessPotential );

        if guild:

            emojis = g_Cache.get( "emojis" );

            emoji = discord.utils.get( guild.emojis, name=ename );

            if emoji:

                uses = emojis.get( ename, 0 );

                uses = uses + 1;

                emojis[ ename ] = uses;

async def manage_emojis() -> None:

    if g_Cache.has_temporal( "emoji_manage" ):
        return;

    from datetime import timedelta;
    g_Cache.set_temporal( "emoji_manage", timedelta( days=7 ) );

    used_emojis = g_Cache.get( "emojis" );

    guild = bot.get_guild( g_Utils.Guild.LimitlessPotential );

    server_emojis = [];

    save_emojis = False;

    for emoji in guild.emojis:

        if not os.path.exists( fmt.join( "emojis/" ) ):

            os.makedirs( fmt.join( "emojis/" ) );

            save_emojis = True;

        if save_emojis:

            url = emoji.url

            extension = url[ url.rfind( "." ) + 1 : ]

            if emoji.animated:

                extension = "gif";

            async with aiohttp.ClientSession() as session:

                async with session.get( url ) as resp:

                    if resp.status == 200:

                        with open( fmt.join( f"emojis/{emoji.name}.{extension}" ), 'wb') as f:

                            f.write( await resp.read() );

        value = used_emojis.get( emoji.name, 0 );

        server_emojis.append( ( emoji, value ) );

    if save_emojis:
        await bot.get_channel( g_Utils.Guild.Channel_BotLogs ).send( "All emojis saved! Make sure to upload more before a week." );
        return;

    server_emojis.sort( key=lambda x: x[1] )

    remove_emojis = random.sample( server_emojis[ : max(10, len( server_emojis ) ) ], k=min( 10, len( server_emojis ) ) );

    embed = discord.Embed( color = 0x196990, timestamp=g_Utils.time )

    embed.title = "Removed emojis for rotation";

    for emoji, used in remove_emojis:

        embed.add_field( inline = False,
            name = emoji.name,
            value = f"{str(emoji)} Uses: {used} times this week"
        );

    used_emojis.clear();

    log_channel = bot.get_channel( g_Utils.Guild.Channel_BotLogs );

    await log_channel.send( embed=embed );

    removed_emojis = [];

    for emoji, used in remove_emojis:

        removed_emojis.append( emoji.name );

        await emoji.delete( reason=f"Least used ({used})" );

    uploaded_emojis = 0;

    new_emojis = [];

    emoji_files = os.listdir( fmt.join( "emojis/" ) );

    random.shuffle( emoji_files );

    for emoji_src in emoji_files:

        file = os.path.join( fmt.join( "emojis/" ), emoji_src );

        if not os.path.isfile( file ):
            continue

        emoji_nam = emoji_src[ : emoji_src.find( "." ) ];

        if emoji_nam in removed_emojis:
            continue; # Don't add emojis we've just removed.

        with open( file, 'rb' ) as img:

            try:

                await guild.create_custom_emoji( name=emoji_nam[:32], image=img.read(), reason="Rotated emoji" );

                new_emojis.append( emoji_nam );

                uploaded_emojis += 1;

            except discord.HTTPException as e:
                pass

    embed2 = discord.Embed( color = 0x196990, timestamp=g_Utils.time )

    embed2.title = "Added emojis for rotation";

    for emoji in guild.emojis:

        if emoji.name in new_emojis:

            embed2.add_field( inline = False,
                name = emoji.name,
                value = str(emoji)
            );

    log_channel = bot.get_channel( g_Utils.Guild.Channel_BotLogs );

    await log_channel.send( embed=embed2 );
