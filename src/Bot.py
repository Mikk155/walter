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

import functools;
from inspect import FrameInfo
from traceback import StackSummary

from typing import Optional;

class Bot( discord.Client ):
#
    dirname: str = '';
    '''Directory path'''

    def __init__( self ) -> None:
    #
        super().__init__( intents = discord.Intents.all() );
        self.tree: CommandTree[Bot] = discord.app_commands.CommandTree( self );
    #

    async def setup_hook( self ) -> None:
    #
        await self.tree.sync();
    #

    def exception( self, func ):
    #
        '''
            Delays a message to the main server's loggin channel when an exception is thrown
        '''

        @functools.wraps( func )
        async def wrapper( *args, **kwargs ):
        #
            try:
            #
                return await func( *args, **kwargs );
            #
            except Exception as e:
            #
                embed: discord.Embed = discord.Embed();

                embed.color = 0xE74C3C;
                embed.title = "Exception";

                if isinstance( e, str ):
                #
                    embed.description = e;
                #
                else:
                #
                    embed.title = str(type(e));
                    embed.description = str(e)
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

                await self.get_channel( 1343235842822504481 ).send( embed=embed, silent=True, mention_author=False, allowed_mentions=False );
            #
        #
        return wrapper;
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
