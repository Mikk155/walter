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

    # Create data for g_PluginManager
    __data__: dict = {};
    __data__["name"] = "Control arase";
    __data__["description"] = "Control arase's horny moments";
    __hooks__: list[Hooks] = [ Hooks.on_message ];
    __data__["hooks"] = __hooks__;

    # Return data for g_PluginManager
    return __data__;

# -TODO Look how to implement server-whitelist on app_commands so this can be easly modifiable
control_yourself = [
    'mommy',
    'mama',
    'sex',
    'gf',
    'feet',
    'armpit',
];

async def on_message( message: discord.Message ) -> int:

    if message.author.id == 768337526888726548:

        try:

            content = message.content.lower();

            for h in control_yourself:

                if h in content:

                    webhook = await message.channel.create_webhook( name='KernCore' );

                    if webhook:

                        user = await bot.fetch_user( 121735805369581570 );

                        avatar = user.avatar.url;

                        if avatar:

                            await webhook.send( content='Control yourself', username='KernCore', avatar_url=avatar );

                        else:

                            await webhook.send( content='Control yourself', username='KernCore', avatar_url=avatar );

                        await webhook.delete()

                    cache = g_Cache.get();

                    cache[ "moment" ] = cache.get( "moment", 0 ) + 1;

                    break;

        except:

            pass;

    return HOOK_CONTINUE();
