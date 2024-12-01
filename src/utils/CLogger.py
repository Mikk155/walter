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

from src.main import *

class CLogger:

    '''
    Class Logger instance
    '''

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

    def __print__( self, type: str, message ) -> str:

        if type:

            message = f'[{type}] {message}';

        if self.__logger__:

            message = f'[{self.__logger__}] {message}';

        return message;

    def warn(self, message) -> str:
        return self.__print__( "warning", message );

    def error(self, message) -> str:
        return self.__print__( "error", message );

    def debug(self, message) -> str:
        return self.__print__( "debug", message );

    def information(self, message) -> str:
        return self.__print__( "information", message );

    def critical(self, message) -> str:
        return self.__print__( "critical", message );
