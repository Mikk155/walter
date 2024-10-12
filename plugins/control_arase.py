from plugins.main import *

control_yourself = [
    'mommy',
    'mama',
    'sex',
    'gf',
    'feet',
    'armpit',
];

async def on_message( message: discord.Message ):

    if message.author.id == 768337526888726548 and message.guild and message.guild.id == 744769532513615922:

        try:

            avatar = None

            user = await bot.fetch_user( 121735805369581570 );

            avatar = user.avatar.url;

            for h in control_yourself:

                if h in message.content:

                    webhook = await message.channel.create_webhook( name='KernCore' );

                    await webhook.send( content='Control yourself', username='KernCore', avatar_url=avatar );

                    await webhook.delete()

                    break;

        except Exception as e:

            return Hook.Continue();

    return Hook.Continue();
