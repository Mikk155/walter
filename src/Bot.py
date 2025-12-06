"""
The MIT License (MIT)

Copyright (c) 2025 Mikk155

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

import discord;
from discord.app_commands.tree import CommandTree;

import os;
from inspect import FrameInfo
from traceback import StackSummary

from typing import Optional;

class Bot( discord.Client ):
#
    dirname: str = '';
    '''Directory path'''

    m_RaisedExceptions: list[discord.Embed] = [];

    def __init__( self ) -> None:
    #
        super().__init__( intents = discord.Intents.all() );
        self.tree: CommandTree[Bot] = discord.app_commands.CommandTree( self );
    #

    async def setup_hook( self ) -> None:
    #
        await self.tree.sync();
    #

    def exception(
        self,
        exception: Exception,
        server: Optional[ discord.Guild | int ] = None,
        returnEmbed: bool = False
    ) -> discord.Embed | None:
    #
        '''
            Delays a message to the main server's loggin channel

            exception: exception that was raised.
                if this is a str there won't be any special formating and we'll use that message.

            server: either discord.Guild or int (guild id) to have an idea where the exception happened.

            returnEmbed: if true it returns a copy of the created embed before the "server" data is applied.
        '''

        embed: discord.Embed = discord.Embed();

        embed.color = 0xE74C3C;
        embed.title = "Exception";

        if isinstance( exception, str ):
        #
            embed.description = exception;
        #
        else:
        #
            embed.title = str(type(exception));
            embed.description = f"{exception}"
        #

        # Append Callback trace
        from sys import exc_info;
        from traceback import extract_tb;

        excType, exc_value, exc_traceback = exc_info();
        tracebackCalls: StackSummary = extract_tb( exc_traceback );

        tracebackCalls.reverse();

        EmbedFields: list[ tuple[ str, str, Optional[bool] ] ] = [];

        for frame in tracebackCalls:
        #
            FrameFilename: str = frame.filename[ frame.filename.rfind( "Python" )
                if ( frame.filename.find( "Python" ) != -1 )
                else len( self.dirname ) : ];

            EmbedFields.append(
                (
                    f'**{excType.__name__}** line: ``{frame.lineno}``',
                    "```py\n{}``` ``{}``".format(
                        frame.line,
                        FrameFilename
                    ),
                    False
                )
            );
        #

        self.AddEmbedFields( embed, EmbedFields );

        embedCopy: discord.Embed | None = embed.copy() if returnEmbed is True else None;

        self.m_RaisedExceptions.append( embed );

        return embedCopy;
    #

    def AddEmbedFields( self, embed: discord.Embed, items: list[ tuple[ str, str, Optional[bool] ] ] ) -> discord.Embed:
    #
        fields = 0;

        for item in items:
        #
            fields += 1;

            if fields > 25:
            #
                self.exception( f"Can not add all fields to the message \"<c>{embed.title}<>\" it's above discord's max capacity of 24 fields!",  );
                break;
            #

            field_title: str = item[0];

            if len( field_title ) > 256:
            #
                field_title = field_title[ : 256 ];
            #

            field_description: str = item[1];

            if len( field_description ) > 1024:
            #
                field_description = field_description[ : 1024 ];
            #

            field_inline: bool | None = item[2] if len(item) > 2 else True;

            embed.add_field( name=field_title, value=field_description, inline=field_inline );
        #
        return embed;
    #
#
