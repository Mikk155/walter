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

#================================================================================================
# Initialise plugins
#================================================================================================

def PluginsInit():

    modulos_path = os.path.join( abspath, "plugins" );

    for file in os.listdir( modulos_path ):

        if file.endswith( ".py" ) and not file.endswith( 'main.py' ):

            try:

                modulo:str = file[ : len(file) - 3 ];

                spec = importlib.util.spec_from_file_location( modulo, os.path.join( modulos_path, file ) );

                obj = importlib.util.module_from_spec( spec );

                spec.loader.exec_module( obj );

                HookManager.module_cache[modulo] = obj

                gpGlobals.__iPlugins__ += 1;

            except Exception as e:

                pre_log_channel( "Error importing plugin {}: {}", [ file, e ] );

PluginsInit();


#================================================================================================
# on_ready
#================================================================================================
@bot.event

async def on_ready():

    await post_log_channel();

    i = gpGlobals.__iPlugins__;
    await log_channel( '{} plugin{} were loaded'.format( 'No' if i <= 0 else 'One' if i == 1 else i, 's' if i > 1 else '' ) );

    await bot.wait_until_ready();

    await log_channel( 'Bot connected and logged as {0.user}{1}'.format( bot, " in developer mode" if gpGlobals.developer else '' ) )

    await HookManager.CallHook( 'on_ready' );

    on_think.start()


#================================================================================================
# on_member_join
#================================================================================================
@bot.event

async def on_member_join( member : discord.Member ):

    await HookManager.CallHook( 'on_member_join', member );


#================================================================================================
# on_think
#================================================================================================
@tasks.loop( seconds = 1 )

async def on_think():

    await bot.wait_until_ready();

    await HookManager.CallHook( 'on_think' );

    gpGlobals.time += 1;


#================================================================================================
# on_member_remove
#================================================================================================
@bot.event

async def on_member_remove( member : discord.Member ):

    await HookManager.CallHook( 'on_member_remove', member );


#================================================================================================
# on_message
#================================================================================================
@bot.event

async def on_message( message: discord.Message ):

    await HookManager.CallHook( 'on_message', message );

#================================================================================================
# on_message_delete
#================================================================================================
@bot.event

async def on_message_delete( message: discord.Message ):

    await HookManager.CallHook( 'on_message_delete', message );


#================================================================================================
# on_message_edit
#================================================================================================
@bot.event

async def on_message_edit( before: discord.Message, after: discord.Message ):

    Args = HookValue();

    Args.edited.before = before;

    Args.edited.after = after;

    await HookManager.CallHook( 'on_message_edit', Args.edited );


#================================================================================================
# on_reaction_add
#================================================================================================
@bot.event

async def on_reaction_add( reaction: discord.Reaction, user : discord.User ):

    Args = HookValue();

    Args.reaction.reaction = reaction;

    Args.reaction.user = user;

    await HookManager.CallHook( 'on_reaction_add', Args.reaction );


#================================================================================================
# on_reaction_remove
#================================================================================================
@bot.event

async def on_reaction_remove( reaction: discord.Reaction, user : discord.User ):

    Args = HookValue();

    Args.reaction.reaction = reaction;

    Args.reaction.user = user;

    await HookManager.CallHook( 'on_reaction_remove', Args.reaction );


#================================================================================================
# log in
#================================================================================================
bot.run( config[ 'DEVELOPER TOKEN' if gpGlobals.developer else 'TOKEN' ] );
