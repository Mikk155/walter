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

        self.m_Logger.info(
            "object.initialized",
            [
                __name__
            ],
            dev=True
        );

    async def setup_hook(self):

        # Don't create commands on github's workflow test run
        from os import getenv;
        if getenv( 'github' ):
            return;

        from src.CConfigSystem import g_Config;
        from src.constdef import INVALID_INDEX, DEVELOPER;

        if DEVELOPER():

            server_id: int = g_Config.configuration[ "server_id" ];

            if server_id == INVALID_INDEX():

                _e_ = self.m_Logger.critical( "bot.run.devmode", [ "server_id" ] );

                raise _e_;

            __MY_GUILD__ = discord.Object( id = server_id );

            self.tree.clear_commands( guild=__MY_GUILD__ );

            self.tree.copy_global_to( guild=__MY_GUILD__ );

            await self.tree.sync( guild=__MY_GUILD__ );

        else:

            await self.tree.sync();

    def get_exception_data(self, v) -> dict:
        '''
        Get a dictionary with data from V (Any discord member)
        '''

        data: dict = {}

#        if isinstance( v, discord.Interaction ) or isinstance( v, discord.Message ) or isinstance( v, discord.text ):

        try:
            if v.channel:
                data["channel_id"] = v.channel.id;
                data["channel"] = v.channel.name;
            if v.guild:
                data["guild_id"] = v.guild.id;
                data["guild"] = v.guild.name;
        except Exception as e:
            pass

        return data;

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

                __json__ = self.get_exception_data( interaction );

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
