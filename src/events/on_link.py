'''
    Event called when a member sends a message containing urls
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import asyncio;
import discord;

async def on_link( message: discord.Message, urls: list[str] ):

    from src.utils.utils import g_Utils;

    try:

        fix_embeds_kvp = {
            # https://github.com/Wikidepia/InstaFix
            "www.instagram.com": "www.ddinstagram.com",

            # https://github.com/FixTweet/FxTwitter
            "https://x.com/": "https://fxtwitter.com/",
        };

        formatted = None;

        for link, replace in fix_embeds_kvp.items():

            if link in message.content:

                if formatted:

                    formatted = formatted.replace( link, replace );

                else:

                    formatted = message.content.replace( link, replace );

        if formatted:

            author = message.author;

            webhook = await bot.webhook( message.channel );

            webhook_message: discord.WebhookMessage = await webhook.send( content=formatted, username=author.display_name, \
                                                                            avatar_url=author.avatar.url if author.avatar else None, wait=True );

            if webhook_message:

                await webhook_message.add_reaction( '✅' );

                await asyncio.sleep(10);

                webhook_message = await message.channel.fetch_message( webhook_message.id );

                if await bot.user_reacted( '✅', message.author, webhook_message ):

                    await webhook_message.clear_reaction( '✅' );

                    bot.deleted_messages.append( message.id );

                    await message.delete();

                else:

                    bot.deleted_messages.append( webhook_message.id );

                    await webhook_message.delete();

    except Exception as e:

        bot.exception( f"command::on_link: {e}", message );
