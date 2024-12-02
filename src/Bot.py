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

    from src.CLogger import CLogger
    m_Logger = CLogger( "BOT" );

    def __init__( self ):

        # Plugins may need all of them, too lazy to create a system for automatizing this.
        super().__init__( intents = discord.Intents.all() )

        self.tree = app_commands.CommandTree( self )

    async def setup_hook(self):

        from os import getenv;
        from sys import argv as args;
        from src.CConfigSystem import g_Config;
        from src.constdef import INVALID_INDEX;

        # Don't create commands on github's workflow test run
        if getenv( 'github' ):
            return;

        if '-dev' in args:

            server_id: int = g_Config.configuration[ "server_id" ];

            if server_id == INVALID_INDEX():
                _e_ = self.m_Logger.critical( "bot.run.devmode", { "arguments": [ "server_id" ] } );
                raise _e_;

            __MY_GUILD__ = discord.Object( id = server_id );

            self.tree.clear_commands( guild=__MY_GUILD__ )
            self.tree.copy_global_to( guild=__MY_GUILD__ )
            await self.tree.sync( guild=__MY_GUILD__ )

        else:

            await self.tree.sync();
