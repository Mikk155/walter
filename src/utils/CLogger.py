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

class CLogger:

    '''
    Class Logger instance
    '''

    from src.main import snippet;

    __logger__: str = None;

    def get_name(self) -> str:

        '''
        Get the logger name
        '''

        return self.__logger__;

    def __init__( self, logger: str ) -> None:

        '''
            Initialise a logger
            **logger**: Name of the logger
        '''

        self.__logger__ = logger;

    def __print__(self, message: str, Logger: snippet | dict = {}) -> str:

        from src.utils.CSentences import g_Sentences;
        from src.constdef import INVALID_INDEX;

        sentence = g_Sentences.get( message );

        __type__ = Logger.get( "type", INVALID_INDEX() );

        if __type__ != INVALID_INDEX():

            __type__ = g_Sentences.get(f"logger.{__type__}");

        sentence = f'[{__type__}] {sentence}';

        if self.__logger__:

            sentence = f'[{self.__logger__}]{sentence}';

        if "arguments" in Logger:

            for __arg__ in Logger[ "arguments" ]:

                sentence = sentence.replace( "{}", str( __arg__ ), 1 );

        if Logger.get( "print console", True ):

            print( sentence );

        #if Logger.get( "print dev", False ):

            # -TODO Print to test server's log channel

        #if Logger.get( "print channel", INVALID_INDEX() ) != INVALID_INDEX():

            # -TODO Print to this provived channel

        #if Logger.get( "print server", INVALID_INDEX() ) != INVALID_INDEX():

            # -TODO Print to this server's log channel

        return sentence;

    def warn(self, message, Logger: snippet | dict = {}) -> str:
        Logger["type"] = "warning";
        return self.__print__( message, Logger );

    def error(self, message, Logger: snippet | dict = {}) -> str:
        Logger["type"] = "error";
        return self.__print__( message, Logger );

    def debug(self, message, Logger: snippet | dict = {}) -> str:
        Logger["type"] = "debug";
        return self.__print__( message, Logger );

    def information(self, message, Logger: snippet | dict = {}) -> str:
        Logger["type"] = "information";
        return self.__print__( message, Logger );

    def critical(self, message, Logger: snippet | dict = {}) -> str:
        Logger["type"] = "critical";
        return self.__print__( message, Logger );

