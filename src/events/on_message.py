from __main__ import bot
from typing import List;
from src.Bot import Bot;
bot: Bot;

import discord;
import asyncio;
from src.const import Colors;

@bot.exception
async def FixEmbeds( message: discord.Message, formatted: str ) -> None:
#
    webhook: discord.Webhook = await bot.webhook( message.channel );

    msg: discord.WebhookMessage = await webhook.send( content=formatted, username=message.author.display_name, \
        avatar_url=message.author.avatar.url if message.author.avatar else None, wait=True );

    reply: discord.Message = await message.reply(
        embed=discord.Embed( color = Colors.LightBlue, description = "Add a reaction if this embed is been fixed." ),
        allowed_mentions=False,
        silent=True
    );    await reply.add_reaction( '✅' );

    async with message.channel.typing():
        await asyncio.sleep( 10 );

    try: # return None? NO! WE HAVE TO RAISE EXCEPTION! :sob:
        reply = await message.channel.fetch_message( reply.id );
    except:
        reply = None;

    if reply is not None:
    #
        if await bot.UserReacted( message.author, reply, emoji='✅' ):
        #
            try: # return None? NO! WE HAVE TO RAISE EXCEPTION! :sob:
                message = await message.channel.fetch_message( message.id );
                await message.delete();
            except: pass;
        #
        else:
        #
            try: # return None? NO! WE HAVE TO RAISE EXCEPTION! :sob:
                msg = await message.channel.fetch_message( msg.id );
                if msg is not None:
                    await msg.delete();
            except: pass;
        #
        await reply.delete();
    #
#

@bot.event
@bot.exception
async def on_message( message: discord.Message ) -> None:
#
    if not message.author:
        return;

    # This is a message from this own bot
    if message.author.id == bot.user.id:
        return;

    # This is a message from a webhook
    if message.webhook_id is not None:
        return;

    # This is a message from a bot
    if message.author.bot:
        return;

    content: str = message.content;

    FixEmbed: str = None;

    if content.find( "//instagram.com" ) != -1:
    #
        FixEmbed = content.replace( "//instagram.com", "//ddinstagram.com", 1 );
    #
    elif content.find( "//x.com" ) != -1:
    #
        FixEmbed = content.replace( "//x.com", "//stupidpenisx.com", 1 );
    #
    elif content.find( "//tiktok.com" ) != -1:
    #
        FixEmbed = content.replace( "//tiktok.com", "//tiktxk.com", 1 );
    #

    if FixEmbed is not None: # Don't queue the code ahead
    #
        task: asyncio.Task = asyncio.create_task( FixEmbeds( message, FixEmbed ) );
    #

    replied: discord.MessageReference | None = message.reference;

    if replied is not None:
    #
        pass;
    #

    mentions: List[discord.User | discord.Member] = message.mentions;

    if len( mentions ) > 0:
    #
        pass;
    #
#
