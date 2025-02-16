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

import os
import discord

from typing import Optional
from discord.ext import commands, tasks
from datetime import timedelta, datetime

from src.utils.Args import argument

#================================================
# Start of Application Commands
#================================================
#================================================
# End of Application Commands
#================================================

#================================================
# Start of BOT
#================================================
class Bot( discord.Client ):

    '''
    Discord BOT instance
    '''

    __on_start_called__: bool = False
    '''Temporal bool to know if this is the first time the bot is run and not a connection recovery.'''

    class ThinkDelta:
        from datetime import datetime
        Secod = datetime
        Minute = datetime
        Hour = datetime
        Day = datetime

    from src.utils.Logger import Logger
    m_Logger: Logger = Logger( "BOT" )

    developer: bool = False
    '''If argument ``-developer`` is ``1`` this will be true.'''

    def __init__( self, developer: bool = False ):
        self.developer = developer
        super().__init__( intents = discord.Intents.all() )
        self.tree = discord.app_commands.CommandTree( self )

    async def setup_hook(self):

        if self.developer:
            __MY_GUILD__ = discord.Object( id = 1145236064596918304 )
            self.tree.clear_commands( guild=__MY_GUILD__ )
            self.tree.copy_global_to( guild=__MY_GUILD__ )
            await self.tree.sync( guild=__MY_GUILD__ )
        else:
            await self.tree.sync()

    def exception( self, exception_obj: ( Exception | str ), ) -> discord.Embed:

        '''
            Build a ``discord.Embed`` class with the stack flow of the exception handled.
        '''

        from src.utils.Logger import LoggerColors, LoggerLevel
        embed = discord.Embed( color = LoggerColors.get( LoggerLevel.error, 0x196990 ), timestamp=datetime.now(), colour=16711680 )

        try:

            from sys import exc_info
            from os.path import abspath
            from traceback import extract_tb

            exc_type, exc_value, exc_traceback = exc_info()
            traceback_list = extract_tb(exc_traceback)

            for frame in traceback_list:
                filename = frame.filename.replace( abspath( "" ), '' )
                if "Python" in filename:
                    filename = filename[ filename.find( "Python" ) : ]
                embed.add_field( inline = False,
                    name = f"{frame.name} line {frame.lineno}",
                    value = f"```py\n{frame.line}``` `{filename}`"
                )

                if len( embed.fields ) > 24:
                    break

                embed.title = exc_type.__name__
                embed.description = str(exception_obj)
                embed.set_footer( text="This incident will be reported." )

        except Exception as e:

            embed = discord.Embed( color = 3447003, timestamp=datetime.now(), title=f'Exception raised during exception builder LOL:', description=e )

        from src.utils.Logger import logs
        logs.append(embed)

        return embed

bot: Bot = Bot( developer = True if argument( "-developer" ) == "true" else False )
#================================================
# End of BOT
#================================================

#================================================
# Start of Events
#================================================
from src.events.on_start import on_start
from src.events.on_resumed import on_resumed
from src.events.on_think import on_think_second, on_think_minute, on_think_hour, on_think_day
from src.events.on_mention import on_mention
from src.events.on_message import on_message as on_sub_message
from src.events.on_reply import on_reply
from src.events.on_link import on_link
from src.events.on_member_join import on_member_join
from src.events.on_member_remove import on_member_remove
from src.events.on_message_delete import on_message_delete
from src.events.on_message_edit import on_message_edit
from src.events.on_reaction import on_reaction, ReactionAction
from src.events.on_invite import on_invite, InviteAction
from src.events.on_typing import on_typing
from src.events.on_guild_channel_pins_update import on_guild_channel_pins_update
from src.events.on_disconnect import on_disconnect
from src.events.on_error import on_error
from src.events.on_guild_emojis_update import on_guild_emojis_update
from src.events.on_guild_stickers_update import on_guild_stickers_update
from src.events.on_audit_log_entry_create import on_audit_log_entry_create

@bot.event
async def on_invite_create( invite: discord.Invite ):
    try:
        await on_reaction( invite, InviteAction.created )
    except Exception as e:
        bot.exception( f"Failed on calling custom hook \"on_invite_create\" Exception: ``{e}``" )

@bot.event
async def on_invite_delete( invite: discord.Invite ):
    try:
        await on_reaction( invite, InviteAction.deleted )
    except Exception as e:
        bot.exception( f"Failed on calling custom hook \"on_invite_delete\" Exception: ``{e}``" )

@bot.event
async def on_reaction_add( reaction: discord.Reaction, user : discord.User ):
    try:
        await on_reaction( reaction, user, ReactionAction.added )
    except Exception as e:
        bot.exception( f"Failed on calling custom hook \"on_reaction_add\" Exception: ``{e}``" )

@bot.event
async def on_reaction_remove( reaction: discord.Reaction, user : discord.User ):
    try:
        await on_reaction( reaction, user, ReactionAction.removed )
    except Exception as e:
        bot.exception( f"Failed on calling custom hook \"on_reaction_remove\" Exception: ``{e}``" )

@bot.event
async def on_message( message: discord.Message ):

    await on_sub_message( message )

    # Contains a mention
    if message.mentions and len( message.mentions ) > 0:
        try:
            await on_mention( message, message.mentions )
        except Exception as e:
            bot.exception( f"Failed on calling custom hook \"on_mention\" Exception: ``{e}``" )

    # is a reply message
    if message.reference and message.reference.message_id:
        try:
            replied_message = await message.channel.fetch_message( message.reference.message_id );
            if replied_message:
                try:
                    await on_reply( message, replied_message )
                except Exception as e:
                    bot.exception( f"Failed on calling custom hook \"on_reply\" Exception: ``{e}``" )
        except discord.NotFound:
            pass;

    # Is a url
    if 'https://' in message.content or 'www.' in message.content:
        contents = message.content.split();
        urls=[]
        for c in contents:
            if c.startswith( 'https://' ) or c.startswith( 'www.' ):
                urls.append( c );
        if len( urls ) > 0:
            try:
                await on_link( message, urls )
            except Exception as e:
                bot.exception( f"Failed on calling custom hook \"on_link\" Exception: ``{e}``" )

@tasks.loop( seconds = 1.0, reconnect=True )
async def think_runner():

    #-TODO Store cache

    await bot.wait_until_ready()

    await on_think_second()

    now = datetime.now(); #-TODO Arg timezone?

    if bot.ThinkDelta.Minute < now:
        await on_think_minute()
        bot.ThinkDelta.Minute = now + timedelta(minutes=1)

    if bot.ThinkDelta.Hour < now:
        await on_think_hour()
        bot.ThinkDelta.Hour = now + timedelta(hours=1)

    if bot.ThinkDelta.Day < now:
        await on_think_day()
        bot.ThinkDelta.Day = now + timedelta(days=1)

    # Print out any delayed logger
    from src.utils.Logger import logs
    if len(logs) > 0:
        log_channel = bot.get_channel( 1211204941490688030 if bot.developer else 1340784821105983508 )
        if log_channel:
            from src.utils.Logger import logs
            amount = 3 # Print only these messages per second
            while len(logs) > 0 and amount > 0:
                if logs[0]:
                    await log_channel.send( embed=logs[0] )
                    await bot.wait_until_ready()
                    amount -= 1
                logs.pop(0)

@bot.event
async def on_ready():

    await bot.wait_until_ready();

    if not bot.__on_start_called__:

        bot.m_Logger.info( f"Bot connected as {bot.user.name}#{bot.user.discriminator}" )

        await on_start()

        now = datetime.now(); #-TODO Arg timezone?
        bot.ThinkDelta.Minute = now + timedelta(minutes=1)
        bot.ThinkDelta.Hour = now + timedelta(hours=1)
        bot.ThinkDelta.Day = now + timedelta(days=1)

        bot.__on_start_called__ = True

    if not think_runner.is_running():

        think_runner.start()

#================================================
# End of Events
#================================================

bot.run( token = open( os.path.join( os.path.dirname( __file__ ), argument( "-token", "token.txt" ) ), "r" ).readline(), reconnect = True )
