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

class g_AppCommands:

    '''
    ``discord.app_commands`` Manager
    '''

    from src.CLogger import CLogger
    m_Logger = CLogger( "Plugin Manager" );

    plugins: dict = {};
    '''Loaded plugins'''

    loaded: int = 0;
    '''Loaded plugins'''


    class CCommandData:

        '''
        app_command data
        '''

        __command_name__: str
        '''app_command name'''

        description: str
        '''
        Command description
        '''

        def __init__( self, command_name: str ):
            '''
            ``command_name`` Name of your command's function
            '''

            from inspect import stack;

            frame = stack()[1]; # Get caller plugin name

            __caller__ = frame.filename;

            for s in [ '\\', '/' ]:

                if s in __caller__:

                    __caller__ = __caller__[ __caller__.rfind( s ) + 1 if __caller__.rfind( s ) != -1 else 0 : len( __caller__ ) ];

            from src.CSentences import g_Sentences;

            if command_name and command_name != '':

                if __caller__ in g_AppCommands.fnMethods():

                    __e__ = g_Sentences.get( "can.not.open" );

                    __exception__ = g_AppCommands.m_Logger.error( "app.command.invalid.name", [ __caller__, __e__ ] );

                    raise Exception( __exception__ );

                else:

                    self.__command_name__ = command_name;

            else:

                from src.utils.format import g_Format;

                __s__ = g_Sentences.get( "can.not.open" );

                __e__ = g_Format.brackets( __s__, [ "command_name" ] );

                g_AppCommands.m_Logger.warn( "app.command.invalid.name", [ __caller__, __e__ ] );

                raise Exception( __exception__ );

    fnMethods: dict[str, list[CCommandData]] = {};

    @staticmethod
    def CreateCommand( command_data: CCommandData ) -> None:
        '''Create an app_command'''

    @staticmethod
    def initialize() -> None:

        from json import dumps;

        g_AppCommands.m_Logger.info(
            "object.initialized",
            [
                __name__
            ],
            dev=True
        );

        g_AppCommands.m_Logger.info(
            "Commands:```json\n{}```",
            [
                dumps(g_AppCommands.fnMethods, indent=2)
            ],
            dev=True
        );
