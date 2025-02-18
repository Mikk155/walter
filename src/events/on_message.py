'''
    Event called when a member sends a message
'''

from __main__ import bot
from src.Bot import Bot
bot: Bot

import discord

from src.utils.CCacheManager import g_Cache
from src.utils.constants import guild_limitlesspotential_id, owner_id

async def on_message( message: discord.Message ):

    # Remove sent messages to #welcome #-TODO Should we use a button + vgui instead of a app command
    if message.guild.id == guild_limitlesspotential_id() and message.channel.id == 1118352656096829530 and not message.author.guild_permissions.administrator:
        await message.delete();

    # Control arase
    if message.author.id == 768337526888726548:
        content = message.content.lower();
        arase_words = [
            'mommy',
            'mama',
            'sex',
            'gf',
            'feet',
            'armpit'
        ]
        for h in arase_words:
            if h in content:
                user = await bot.fetch_user( 121735805369581570 );
                avatar = user.avatar.url;
                cache = g_Cache.get( "control_arase" );
                number = cache.get( "times", 0 );
                number += 1;
                cache[ "times" ] = number;
                webhook = await bot.webhook( message.channel )
                await webhook.send( content='Control yourself', username='KernCore', avatar_url=avatar );
                break;

    # Neko marry sara
    elif message.author.id == owner_id():
        content = message.content.lower();
        if 'neko marry' in content:
            sare: discord.User = bot.get_guild( guild_limitlesspotential_id() ).get_member( 746914044828450856 );
            if sare and sare in message.mentions:
                cache = g_Cache.get( "marry_sare" );
                number = cache.get( "times", 52 );
                number += 1;
                await bot.get_channel( message.channel.id ).send( f"Mikk has confesed his love to Sare {number} times.", mention_author=False );
                cache[ "times" ] = number;
