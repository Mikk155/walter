from src.main import *

def on_initialization( plugin: Plugin ) -> Plugin:
    '''
    Called when the script is executed, this is the first hook ever called.

    The bot is not even initialized yet.

    This hook is required on all plugins and must return data.

    Change members of the ``plugin`` variable and then return it.

    you can do extra stuff in here for initialization too.
    '''

    plugin.name = "Test"

    plugin.hooks.append( Hooks.on_message )

    return plugin;

async def on_message( message: discord.Message ) -> int:

    if message.author.id == 744768007892500481 and message.guild and message.guild.id == 1145236064596918304:

        await message.reply( "Si carajo" )

    return HOOK_CONTINUE();
