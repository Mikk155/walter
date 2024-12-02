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

#=======================================================================================
# Start initialization of required libraries
#=======================================================================================

def initialize() -> None:

    g_Sentences.initialize();
    g_Config.initialize();
    g_PluginManager.initialize();

initialize();

bot = Bot();

#=======================================================================================
# END
#=======================================================================================

#=======================================================================================
# on_ready
#=======================================================================================

@bot.event
async def on_ready():

    await bot.wait_until_ready();

    bot.m_Logger.info(
        'bot.on.ready',
        [
            bot.user.name,
            bot.user.discriminator
        ],
        dev=True
    );

    if os.getenv( 'github' ):

        print( "Run from {}".format( os.getenv( 'github' ) ) );

        await bot.close();

        exit(0);

    on_think.start()

#=======================================================================================
# END
#=======================================================================================

#=======================================================================================
# on_ready
#=======================================================================================

@tasks.loop( seconds = 1 )
async def on_think():

    await bot.wait_until_ready();

    if g_DelayedLog.should_print():
        await g_DelayedLog.print_server(bot);

#=======================================================================================
# END
#=======================================================================================

#=======================================================================================
# run bot
#=======================================================================================

def get_token() -> str:

    __token__: list[str] = [ INVALID_INDEX(), INVALID_INDEX() ];

    if os.getenv( 'github' ):

        __token__[0] = os.getenv( 'token' );

    else:

        tokens: str = g_Path.join( 'tokens.txt' );

        if os.path.exists( tokens ):

            __token__ = open( tokens, 'r' ).readlines();

        else:

            bot.m_Logger.critical( "file.not.exists", [ tokens ] );

            exit(0)

    token = __token__[ 1 if '-dev' in sys.argv else 0 ];

    if not isinstance( token, str ):

        token = str(token);

    return token;

try:

    bot.run( token = get_token(), reconnect = True );

except Exception as e:

    bot.m_Logger.critical( e );

#=======================================================================================
# END
#=======================================================================================
