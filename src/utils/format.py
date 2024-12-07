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

class g_Format:

    '''
    Formatting utilities
    '''

    from src.CLogger import CLogger
    m_Logger = CLogger( "Formating" );

    @staticmethod
    def brackets(sentence:str, args: list = []) -> str:

        for __arg__ in args:

            sentence = sentence.replace( "{}", str( __arg__ ), 1 );

        return sentence;

    from discord import app_commands
    def to_command_choices( obj: dict[str, str] | list[str] ) -> list[app_commands.Choice]:

        '''
        Converts a dictionary to a list of app_commands.Choice
        '''

        from discord import app_commands

        icount = 0;

        app_commands_choices = [];

        for k, v in obj.items() if isinstance( obj, dict ) else enumerate( obj ):

            if icount >= 25:

                g_Format.m_Logger.warn( "format.command_choices.bigger" );

                break;

            icount += 1;

            if isinstance( k, int ):

                app_commands_choices.append( app_commands.Choice( name=v, value=str(k) ) );

            else:

                app_commands_choices.append( app_commands.Choice( name=k, value=v ) );

        return app_commands_choices;

    from discord import Member
    def user_mention( user: Member ) -> str:
        '''
        Return a fixed ``discord.Member.mention`` string for globalization\n
        since a leading characters are added when the user has a custom nickname
        '''

        if user:

            if isinstance( user, int ):

                return f"<@{user}>";

            else:

                return f"<@{user.id}>";

        g_Format.m_Logger.warn( "format.invalid.mention" );

        return "";
