from plugins.main import *

hooks = [
    Hooks.on_message
];

RegisterHooks( __file__, hook_list=hooks );

global fix_embeeds_kvp;
fix_embeeds_kvp = {
    # https://github.com/Wikidepia/InstaFix
    "www.instagram.com": "www.ddinstagram.com",

    # https://github.com/FixTweet/FxTwitter
    "https://x.com/": "https://fxtwitter.com/",
};

async def on_message( message: discord.Message ):

    for link, replace in fix_embeeds_kvp.items():
        if link in message.content:

            author = message.author.mention;

            formatted = message.content.replace( link, replace );

            await message.channel.send(  '{}: {}'.format( author, formatted ) );

            await message.delete();

    return ReturnCode.Continue;
