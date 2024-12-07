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

import discord
from discord import app_commands

class Bot( discord.Client ):

    '''
    Discord BOT instance
    '''

    __on_start_called__: bool = False

    from src.CLogger import CLogger
    m_Logger = CLogger( "BOT" );

    def __init__( self ):

        # Plugins may need all of them, too lazy to create a system for automatizing this.
        super().__init__( intents = discord.Intents.all() )

        self.tree = app_commands.CommandTree( self )

        from src.constdef import DEVELOPER;

        if not DEVELOPER():

            self.m_Logger.info(
                "object.initialized",
                [
                    __name__
                ],
                dev=True
            );

    async def setup_hook(self):

        from src.CConfigSystem import g_Config;
        from src.constdef import DEVELOPER;

        if DEVELOPER():

            if not "developer_guild" in g_Config.configuration:

                _e_ = self.m_Logger.critical( "bot.run.devmode", [ "developer->guild->int" ] );

                raise Exception( _e_ );

            __MY_GUILD__ = discord.Object( id = g_Config.configuration[ "developer_guild" ] );

            self.tree.clear_commands( guild=__MY_GUILD__ );

            self.tree.copy_global_to( guild=__MY_GUILD__ );

            await self.tree.sync( guild=__MY_GUILD__ );

        else:

            await self.tree.sync();

        g_Config.configuration.pop( "developer_guild", None );

    async def exception_handle( self, exception: ( Exception | str ), interaction: ( discord.Interaction | discord.Member | discord.TextChannel ) = None, additional_commentary: str = None, concurrent: bool = False ) -> None:
        '''
        Handles an exception.

        ``exception`` The exception that happened.

        ``additional_commentary`` Any additional commentary to print after the message.

        ``interaction`` If provided, the interaction response will be updated.

        ``concurrent`` if true, this exception won't be send to the developer discord's log channel
        '''

        try:

            from src.CSentences import g_Sentences;
            from src.utils.format import g_Format;

            if not concurrent:

                __ext_fmt__ = '';

                __json__: dict = {}

                if interaction:

                    try:
                        if interaction.channel:
                            __json__["channel_id"] = interaction.channel.id;
                            __json__["channel"] = interaction.channel.name;
                        if interaction.guild:
                            __json__["guild_id"] = interaction.guild.id;
                            __json__["guild"] = interaction.guild.name;
                    except Exception as e:
                        pass

                from sys import exc_info;
                from src.utils.Path import g_Path;
                from traceback import extract_tb;

                exc_type, exc_value, exc_traceback = exc_info()

                last_frame = extract_tb(exc_traceback)[-1]

                __json__[ "file" ] = last_frame.filename.replace( g_Path.workspace(), '' );
                __json__[ "caller" ] = last_frame.name;
                __json__[ "line" ] = last_frame.lineno;
                __json__[ "exception" ] = str(exception);

                if len(__json__) > 0:
                
                    __ext__ = g_Sentences.get( "bot.handle.exception.server" );

                    from json import dumps;

                    __dump__ = dumps( __json__, indent=2 );

                    __ext_fmt__ = g_Format.brackets( __ext__, [ __dump__ ] );

                self.m_Logger.warn(
                    "bot.handle.exception.dev",
                    [
                        exception,
                        __ext_fmt__,
                        additional_commentary if additional_commentary else ''
                    ],
                    dev=True
                );

            if interaction:

                if isinstance( interaction, discord.Interaction ):

                    __trans__ = g_Sentences.get( "bot.handle.exception", interaction.guild_id );

                    msg = g_Format.brackets( __trans__, [ exception ] );

                    if additional_commentary:

                        msg = f'{msg}\n{additional_commentary}';

                    await interaction.followup.send( msg );

                # if not concurrent:
                    # -TODO Try to reply to the user that raised this exception

        except Exception as e:

            print(e)
            pass

    from datetime import datetime
    from src.constdef import INVALID_INDEX
    def time(self, server_id = INVALID_INDEX() ) -> datetime:

        from datetime import datetime as dt;
        from src.constdef import INVALID_INDEX;
        from pytz import timezone, UnknownTimeZoneError, UTC;

        '''
        Get bot's date time now
        
        ``server_id`` Get the datetime for this server
        '''

        default_timezone = 'UTC'

        time = None;

        if server_id != INVALID_INDEX:

            from src.CCacheManager import g_Cache;

            cache = g_Cache.get( "timezone.py" );

            if str( server_id ) in cache:

                timezone_name = cache.get( str( server_id ), default_timezone );

                try:

                    timezone = timezone( timezone_name );

                except UnknownTimeZoneError:

                    timezone = timezone( default_timezone );

                time = dt.now( timezone );
        
        return time if time else dt.now();
