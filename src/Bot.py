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

        self.m_Logger.info( "object_initialized", [ __name__ ], dev=True );

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

    from typing import Optional
    async def exception_handle( \
            self,
            exception: ( Exception | str ),
            interaction = None,
            additional_commentary: Optional[str] = None,
            concurrent: Optional[bool] = None
        ) -> None:
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

            embed = discord.Embed( color = 3447003, timestamp=self.time(), colour=16711680 );

            if additional_commentary:
                embed.add_field( inline = False, name = "app commentary", value = additional_commentary );

            if interaction:
                channel_target: discord.TextChannel = None;
                if isinstance( interaction, discord.TextChannel  ):
                    channel_target = interaction;
                else: # Assume is a message/interaction
                    try:
                        channel_target = interaction.channel;
                    except Exception as e:
                        pass
                try:
                    if channel_target:
                        embed.add_field( inline = False, name = "channel_id", value = f"{channel_target.id}" );
                        embed.add_field( inline = False, name = "channel", value = f"{channel_target.name}" );
                        if channel_target.guild:
                            embed.add_field( inline = False, name = "guild_id", value = f"{channel_target.guild.id}" );
                            embed.add_field( inline = False, name = "channel", value = f"{channel_target.guild.name}" );
                except Exception as e:
                    pass

                from sys import exc_info;
                from src.utils.Path import g_Path;
                from traceback import extract_tb;

                exc_type, exc_value, exc_traceback = exc_info()
                traceback_list = extract_tb(exc_traceback)

                for frame in traceback_list:
                    filename = frame.filename.replace( g_Path.workspace(), '' );
                    if "Python" in filename:
                        filename = filename[ filename.find( "Python" ) : ];
                    embed.add_field( inline = False,
                        name = f"{frame.name} line {frame.lineno}",
                        value = f"```py\n{frame.line}``` `{filename}`"
                    );

                    if len( embed.fields ) > 24:
                        break;

                embed.title = exc_type.__name__;
                embed.description = str(exception);
                embed.set_footer( text="message sent to devs" );

                if not concurrent:

                    from src.CConfigSystem import g_Config;
                    await self.get_channel( g_Config.configuration["log_channel"]).send( embed=embed );

                msg = g_Sentences.get( "bot.handle.exception", interaction.guild_id );

                if isinstance( interaction, discord.Interaction ):

                    await interaction.followup.send( msg, embed=embed );

                elif not concurrent:

                    if isinstance( interaction, discord.Message ):

                        await interaction.reply( msg, embed=embed, mention_author=False );

                    elif isinstance( interaction, discord.TextChannel ):

                        await interaction.send( msg, embed=embed );

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
