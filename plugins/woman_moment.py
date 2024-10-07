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

from plugins.main import *

async def on_message( message: discord.Message ):

    if message.guild and message.guild.id == 744769532513615922 and 'woman moment' in message.content:

        bunnt: discord.User = bot.get_guild( 744769532513615922 ).get_member( 740196277844967458 );

        if bunnt:

            number = str( int( open( '{}woman_moment.txt'.format( gpGlobals.absp() ), 'r' ).readline() ) + 1 );

            nombre_actual = bunnt.display_name;

            moment = re.sub( r'\d+', str(number), nombre_actual )

            if not str(number) in moment:

                moment = '{} {}'.format( moment, number );

            await bunnt.edit( nick=moment)

            open( '{}woman_moment.txt'.format( gpGlobals.absp()  ), 'w' ).write( number );
