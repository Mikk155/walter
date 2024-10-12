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

@bot.tree.command()
@app_commands.describe( plugin='Plugin' )
@app_commands.choices( plugin = gpUtils.to_command_choices( g_PluginManager.__PluginsNames__ ) )
async def plugin_info( interaction: discord.Interaction, plugin: app_commands.Choice[str] ):
    """Show plugins information"""

    try:

        info = g_PluginManager.__PluginsData__[ plugin.value ];

        msg = 'Plugin: ``{}``\n'.format( info[ "File Name" ] )

        msg += 'Active: ``{}``\n'.format( '❌' if info.get( "Disable", False ) else '✅' );

        if 'Plugin Name' in info:
            msg += 'Name: ``{}``\n'.format( info[ "Plugin Name" ] );

        if 'Author Name' in info:
            msg += 'Author: ``{}``\n'.format( info[ "Author Name" ] );

        if 'Author Contact' in info:
            msg += 'Contact: {}\n'.format( info[ "Author Contact" ] );

        if 'Description' in info:
            msg += 'Description: ``{}``\n'.format( info[ "Description" ] );

        if 'Hooks' in info:
            msg += 'Hooks: ``{}``\n'.format( info[ "Hooks" ] );

        await interaction.response.send_message( msg );

    except Exception as e:

        await interaction.response.send_message( "Exception {}".format( e ) );

@bot.tree.command()
@app_commands.describe( language='Language' )
@app_commands.choices( language = gpUtils.to_command_choices( sentences[ "languages" ] ) )
async def cfg_language( interaction: discord.Interaction, language: app_commands.Choice[str] ):
    """Set bot language for this server"""

    try:

        if interaction.user.guild_permissions.administrator:

            cache = gpGlobals.cache.get();

            server_cache = cache.get( str( interaction.guild_id ), {} );

            server_cache[ "language" ] = language.name

            cache[ str( interaction.guild_id ) ] = server_cache;

            await interaction.response.send_message( AllocString( "language.updated", [ language.name ], interaction.guild_id ) );
    
        else:

            await interaction.response.send_message( AllocString( "no.permission", [ "administrator" ], interaction.guild_id ) );

    except Exception as e:

        await interaction.response.send_message( "Exception {}".format( e ) );

@bot.event
async def on_ready():
    await bot.post_log_channel( g_PluginManager.num_plugins() );
    await bot.wait_until_ready();
    await g_PluginManager.CallHook( 'on_ready' );

    if gpGlobals.workflow():
        await g_PluginManager.CallHook( 'on_think' ); # Call on_think once
        await bot.log_channel( "All tests ended, Shutting down bot." );
        await bot.close();
        exit(0);
    elif gpGlobals.time() == 0:
        on_think.start()

@bot.event
async def on_member_join( member : discord.Member ):
    await g_PluginManager.CallHook( 'on_member_join', member );

@tasks.loop( seconds = 1 )
async def on_think():
    await bot.wait_until_ready();
    await g_PluginManager.CallHook( 'on_think' );
    gpGlobals.__time__ += 1;
    await bot.hook_on_think();

@bot.event
async def on_member_remove( member : discord.Member ):
    await g_PluginManager.CallHook( 'on_member_remove', member );

@bot.event
async def on_message( message: discord.Message ):
    await bot.hook_on_message( message );
    await g_PluginManager.CallHook( 'on_message', message );

@bot.event
async def on_message_delete( message: discord.Message ):
    await g_PluginManager.CallHook( 'on_message_delete', message );

@bot.event
async def on_message_edit( before: discord.Message, after: discord.Message ):
    await g_PluginManager.CallHook( 'on_message_edit', before, after );

@bot.event
async def on_reaction_add( reaction: discord.Reaction, user : discord.User ):
    await g_PluginManager.CallHook( 'on_reaction_add', reaction, user );

@bot.event
async def on_reaction_remove( reaction: discord.Reaction, user : discord.User ):
    await g_PluginManager.CallHook( 'on_reaction_remove', reaction, user  );

Token: str;

if gpGlobals.workflow():

    Token = os.getenv( 'TOKEN' );

else:

    Token_Name = 'dev' if gpGlobals.developer() else 'token';

    Token_Path = '{}/{}.txt'.format( gpGlobals.abs(), Token_Name );

    if not os.path.exists( Token_Path ):
        print( 'File {} doesn\'t exists! Exiting...' );
        exit(1);

    Token_File = open( Token_Path, 'r' ).readlines();

    Token = Token_File[0];

bot.run( Token );
