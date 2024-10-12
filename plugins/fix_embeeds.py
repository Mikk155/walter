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

global fix_embeeds_kvp;
fix_embeeds_kvp = {
    # https://github.com/Wikidepia/InstaFix
    "www.instagram.com": "www.ddinstagram.com",

    # https://github.com/FixTweet/FxTwitter
    "https://x.com/": "https://fxtwitter.com/",
};

async def on_link( message: discord.Message, urls: list[str] ):

    for link, replace in fix_embeeds_kvp.items():

        if link in message.content:

            author = message.author;

            formatted = message.content.replace( link, replace );

            avatar = author.avatar.url if author.avatar else None;

            username = author.display_name;

            webhook = await message.channel.create_webhook(name='fixembed_cmd')

            await webhook.send( content=formatted, username=username, avatar_url=avatar );

            await message.delete();

            await webhook.delete();

    return Hook.Continue();
