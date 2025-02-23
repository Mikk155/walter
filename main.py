"""
The MIT License (MIT)

Copyright (c) 2024 Mikk155

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import sys;

def argument( name: str, default: str = None ) -> None | str:
    if name in sys.argv and len(sys.argv) > sys.argv.index( name ):
        return sys.argv[ sys.argv.index( name ) + 1 ]
    return default

developer = argument( "-developer" ) == "true";

import os;
import discord;

from typing import Optional;
from discord.ext import commands, tasks;
from datetime import timedelta;

from src.utils.sentences import sentences
from src.utils.utils import g_Utils;

from src.Bot import Bot as DiscordBot;
bot: DiscordBot = DiscordBot();

#================================================
# Start of Application Commands
#================================================
import src.commands.Activity;
import src.commands.cache;
import src.commands.ping_count;
import src.commands.count_together;
import src.commands.say;
import src.commands.minesweeper;
#================================================
# End of Application Commands
#================================================

from src.utils.CCacheManager import g_Cache;

g_Cache.initialize();

#bot.m_Logger.trace( sentences[ "OBJECT_INITIALISED" ], "Cache System" ).print();

#================================================
# Start of Events
#================================================
from src.events.on_start import on_start;
from src.events.on_resumed import on_resumed;
from src.events.on_think_second import on_think_second
from src.events.on_think_minute import on_think_minute
from src.events.on_think_hour import on_think_hour
from src.events.on_think_day import on_think_day
from src.events.on_mention import on_mention;
from src.events.on_message import on_message as on_sub_message;
from src.events.on_reply import on_reply;
from src.events.on_link import on_link;
from src.events.on_member_join import on_member_join;
from src.events.on_member_remove import on_member_remove;
from src.events.on_message_delete import on_message_delete;
from src.events.on_message_edit import on_message_edit;
from src.events.on_reaction import on_reaction, ReactionAction;
from src.events.on_invite import on_invite, InviteAction;
from src.events.on_typing import on_typing;
from src.events.on_guild_channel_pins_update import on_guild_channel_pins_update;
from src.events.on_disconnect import on_disconnect;
from src.events.on_error import on_error;
from src.events.on_guild_emojis_update import on_guild_emojis_update;
from src.events.on_guild_stickers_update import on_guild_stickers_update;
from src.events.on_audit_log_entry_create import on_audit_log_entry_create;

@bot.event
async def on_invite_create( invite: discord.Invite ):

    try:

        await on_invite( invite, InviteAction.created );

    except Exception as e:

        bot.exception( sentences[ "EVENT_FAIL_CALL_CUSTOM_HOOK" ].format( "on_invite_create", e ) );

@bot.event
async def on_invite_delete( invite: discord.Invite ):

    try:

        await on_invite( invite, InviteAction.deleted );

    except Exception as e:

        bot.exception( sentences[ "EVENT_FAIL_CALL_CUSTOM_HOOK" ].format( "on_invite_delete", e ) );

@bot.event
async def on_reaction_add( reaction: discord.Reaction, user : discord.User ):

    try:

        await on_reaction( reaction, user, ReactionAction.added );

    except Exception as e:

        bot.exception( sentences[ "EVENT_FAIL_CALL_CUSTOM_HOOK" ].format( "on_reaction_add", e ) );

@bot.event
async def on_reaction_remove( reaction: discord.Reaction, user : discord.User ):

    try:

        await on_reaction( reaction, user, ReactionAction.removed );

    except Exception as e:

        bot.exception( sentences[ "EVENT_FAIL_CALL_CUSTOM_HOOK" ].format( "on_reaction_remove", e ) );

@bot.event
async def on_message( message: discord.Message ):

    await on_sub_message( message );

    # Contains a mention
    if message.mentions and len( message.mentions ) > 0:

        try:

            await on_mention( message, message.mentions );

        except Exception as e:

            bot.exception( sentences[ "EVENT_FAIL_CALL_CUSTOM_HOOK" ].format( "on_mention", e ) );

    # is a reply message
    if message.reference and message.reference.message_id:

        try:

            replied_message = await message.channel.fetch_message( message.reference.message_id );

            if replied_message:

                try:

                    await on_reply( message, replied_message );

                except Exception as e:

                    bot.exception( sentences[ "EVENT_FAIL_CALL_CUSTOM_HOOK" ].format( "on_reply", e ) );

        except discord.NotFound:

            pass;

    # Is a url
    if 'https://' in message.content or 'www.' in message.content:

        contents = message.content.split();

        urls=[];

        for c in contents:

            if c.startswith( 'https://' ) or c.startswith( 'www.' ):

                urls.append( c );

        if len( urls ) > 0:

            try:

                await on_link( message, urls );

            except Exception as e:

                bot.exception( sentences[ "EVENT_FAIL_CALL_CUSTOM_HOOK" ].format( "on_link", e ) );

@tasks.loop( seconds = 1.0, reconnect=True )
async def think_runner():

    g_Cache.__update__();

    await bot.wait_until_ready();

    last_time = g_Cache.get( "timedelta" );

    time = g_Utils.time;

    await on_think_second( time );

    if last_time.get( "minute", 0 ) != time.minute:
        last_time[ "minute" ] = time.minute;
        await on_think_minute( time );

    if last_time.get( "hour", 0 ) != time.hour:
        last_time[ "hour" ] = time.hour;
        await on_think_hour( time );

    if last_time.get( "day", 0 ) != time.day:
        last_time[ "day" ] = time.day;
        await on_think_day( time );

    # Print out any delayed logger
    from src.utils.Logger import logs;

    if len(logs) > 0:

        log_channel = bot.get_channel( g_Utils.Guild.Channel_BotLogs );

        if log_channel:

            from src.utils.Logger import logs;

            embeds: list[discord.Embed] = []

            amount = 3; # Print only these messages per second

            while amount > 0:

                while len(embeds) < 10 and len(logs) > 0:

                    if logs[0]:

                        embeds.append( logs[0] );

                        logs.pop(0);

                    else:

                        break;

                if len( embeds ) > 0:

                    await log_channel.send( embeds = embeds, silent = True );

                    embeds.clear();

                    await bot.wait_until_ready();
                
                else:

                    break;

                amount -= 1;

@bot.event
async def on_ready():

    await bot.wait_until_ready();

    from src.plugins.Roles import role_view_setup;
    await role_view_setup();

    if not bot.__on_start_called__:

        bot.m_Logger.info( sentences[ "EVENT_ON_START" ].format( bot.user.name, bot.user.discriminator ) ).print();

        bot.timedelta = g_Utils.time;

        await bot.update_invites();

        await on_start();

        bot.__on_start_called__ = True;

    if not think_runner.is_running():

        think_runner.start();

#================================================
# End of Events
#================================================

bot.run( token = open( os.path.join( os.path.dirname( __file__ ), argument( "-token", "token.txt" ) ), "r" ).readline(), reconnect = True );
