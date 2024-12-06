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

def on_initialization() -> dict:
    '''
    Called when the script is executed, this is the first hook ever called.

    The bot is not even initialized yet.

    This hook is required on all plugins and must return data.
    '''

    __data__: dict = {};
    __data__["name"] = "neko marry";
    __data__["description"] = "Count how many times mikk confessed his love to the goddess sara";
    __hooks__: list[Hooks] = [ Hooks.on_message ];
    __data__["hooks"] = __hooks__;

    return __data__;

async def on_message( message: discord.Message ) -> int:

    if message.author.id == 744768007892500481:

        content = message.content.lower();

        if 'neko marry' in content:

            sare: discord.User = bot.get_guild( 744769532513615922 ).get_member( 746914044828450856 );

            if sare and sare in message.mentions:

                cache = g_Cache.get();

                number = cache.get( "times", 52 );

                number += 1;

                await bot.get_channel( message.channel.id ).send( f"Mikk has confesed his love to Sare {number} times.", mention_author=False );

                cache[ "times" ] = number;

    return HOOK_CONTINUE();
