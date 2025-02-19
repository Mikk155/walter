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
from src.utils.utils import g_Utils

global logs
logs: list[discord.Embed] = []

global LogLevel;
LogLevel: int = -1;

class LoggerLevel:

    '''
    Logger level settings
    '''

    none = 0;
    all_logs = -1;
    trace = ( 1 << 0 );
    warning = ( 1 << 1 );
    information = ( 1 << 2 );
    debug = ( 1 << 3 );
    error = ( 1 << 4 );
    critical = ( 1 << 5 );

    @staticmethod
    def set( LoggerLevel: int ) -> None:
        '''Set a Logger level'''
        global LogLevel;
        LogLevel |= LoggerLevel;

    @staticmethod
    def clear( LoggerLevel: int ) -> None:
        '''Clear a Logger level'''
        global LogLevel;
        LogLevel &= ~ LoggerLevel;

global LoggerColors;
LoggerColors = {
    LoggerLevel.debug: 0x808080,
    LoggerLevel.trace: 0x800080,
    LoggerLevel.information: 0x00FF00,
    LoggerLevel.warning: 0xFFFF00,
    LoggerLevel.error: 0xFF0000,
    LoggerLevel.critical: 0xFF0000,
};

class LoggerEmbed( discord.Embed ):

    should_log = False;

    cmd_string = '';

    def print( self ) -> bool:
        '''Try to print the loggig channel. if the log level is disabled returns false'''
        if self.should_log:
            global logs;
            logs.append( self );
        print( self.cmd_string );
        return self.should_log;

class Logger():

    '''
    Logger instance
    '''

    module: str = None;

    def __init__( self, module_name: str = None ):
        self.module = module_name;

    def __logger__( self, emoji: str, type: str, string: str, LoggerLevel: LoggerLevel, *args ) -> LoggerEmbed:

        for arg in args:
            if not '{}' in string:
                break;
            string = string.replace( "{}", arg if isinstance( arg, str ) else str(arg), 1 );

        embed = LoggerEmbed( color=LoggerColors.get( LoggerLevel, 0x196990 ), timestamp=g_Utils.time(), title=f'{emoji} [{self.module}] {type}' if self.module else f'{emoji} {type}', description=string )
        embed.cmd_string = '[{}] {}'.format( f'{self.module}::{type}' if self.module else type, string );

        global LogLevel;
        if LogLevel == -1 or LogLevel & ( LoggerLevel ):

            embed.should_log = True

        return embed;

    def error( self, string: str, *args ) -> LoggerEmbed:
        return self.__logger__( "‼️", "Error", string, LoggerLevel.error, *args );

    def debug( self, string: str, *args ) -> LoggerEmbed:
        return self.__logger__( "📝", "Debug", string, LoggerLevel.debug, *args );

    def warn( self, string: str, *args ) -> LoggerEmbed:
        return self.__logger__( "⚠️", "Warning", string, LoggerLevel.warning, *args );

    def info( self, string: str, *args ) -> LoggerEmbed:
        return self.__logger__( "❕", "Info", string, LoggerLevel.information, *args );

    def trace( self, string: str, *args ) -> LoggerEmbed:
        return self.__logger__( "➡", "Trace", string, LoggerLevel.trace, *args );

    def critical( self, string: str, *args ) -> LoggerEmbed:
        return self.__logger__( "⛔", "Critical", string, LoggerLevel.critical, *args );
