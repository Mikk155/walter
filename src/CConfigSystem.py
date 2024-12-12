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

class g_Config:

    '''
    Configuration System
    '''

    from src.CLogger import CLogger
    m_Logger = CLogger( "Configuration System" );

    configuration: dict = {};
    '''General configuration'''

    plugins: dict = {};
    '''Loaded plugins'''

    @staticmethod
    def initialize() -> None:

        from src.utils.Path import g_Path;
        from src.utils.CJsonCommentary import jsonc;
        from src.constdef import INVALID_INDEX;

        __config__ = jsonc.load( g_Path.join( "config.json" ) )

        if "guild" in __config__.get( "developer", {} ):

            g_Config.configuration[ "developer_guild" ] = __config__.get( "developer", {} )[ "guild" ];

        if "token" in __config__.get( "developer", {} ):

            g_Config.configuration[ "token_dev" ] = __config__.get( "developer", {} )[ "token" ];

        loggers = __config__.get( "loggers", [ "debug", "warning", "info", "trace" ] );

        # These are required.
        loggers.append( "critical" );
        loggers.append( "error" );

        g_Config.configuration[ "loggers" ] = loggers;

        g_Config.configuration[ "log_channel" ]     = __config__.get( "log_channel", INVALID_INDEX() );
        g_Config.configuration[ "owner" ]   = __config__.get( "owner", INVALID_INDEX() );
        g_Config.configuration[ "token" ]   = __config__.get( "token", INVALID_INDEX() );

        g_Config.plugins = __config__.get( "plugins", [] );

        g_Config.m_Logger.info( "object_initialized", [ __name__ ], dev=True );
