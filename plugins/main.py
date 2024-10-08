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

#=======================================================================================
# All the libraries being used for either this main script or plugins
#=======================================================================================
import os
import re
import sys
import time
import json
import random
import asyncio
import discord
import requests
import subprocess
import importlib
from git import Repo
import importlib.util
from typing import Optional
from datetime import datetime
from discord import app_commands
from discord.ext import commands, tasks
from bs4 import BeautifulSoup

#=======================================================================================
# Global Public variables
#=======================================================================================
global gpGlobals
class gpGlobals:
    '''Global variables'''

    @staticmethod
    def abs() -> str:
        '''Return absolute path value to the bot folder'''
        return '{}/'.format( os.path.abspath( "" ) );

    @staticmethod
    def absp() -> str:
        '''Return absolute path value to the plugins folder'''
        return '{}plugins/'.format( gpGlobals.abs() );

    __time__ = 0;
    @staticmethod
    def time() -> int:
        '''Current time of think.\n\nThis increases in 1 each second.'''
        return gpGlobals.__time__;

    __developer__ = True if '-dev' in sys.argv else False;
    @staticmethod
    def developer() -> bool:
        '''Returns **True** If the bot has been run by using the ``-dev`` argument'''
        return gpGlobals.__developer__;

    __git_workflow__ = True if '-github' in sys.argv else False;
    @staticmethod
    def workflow() -> bool:
        '''App has been run from Github's workflows'''
        return gpGlobals.__git_workflow__;

    @staticmethod
    def should_think( var: int, next_think: int ) -> ( bool, int ): # type: ignore
        '''
        Returns whatever this is the time to think

        ``var``: a global variable of your own for comparing

        ``next_think``: cooldown in seconds till this function should return true
        '''
        if var > gpGlobals.time():
            return False, var;
        var = gpGlobals.time() + next_think;
        return True, var;

#=======================================================================================
# Global Public Utilities
#=======================================================================================
global gpUtils;
class gpUtils:
    '''General Utilities'''

    def mention( user: discord.Member | str ) -> str:
        '''Return a fixed ``discord.Member.mention`` string for globalization\n\nsince a leading ``!`` is added when the user has a nickname'''
        mention = user.mention if isinstance( user, discord.Member ) else user;

        if mention.find( '!' ) != -1:
            mention = mention.replace( '!', '' );
    
        return mention;

    def get_time( seconds : int ) -> str:
        '''Get time in a ``hh:mm:ss`` format'''
        m = seconds // 60;
        sr = seconds % 60;
        return f"{m}m:{sr:02d}s";

    def jsonc( obj : list[str] | str ) -> dict | list:
        '''Open a json file ignoring single-line commentary\n
        Returns empty dict if an Exception is thrown\n
        **obj** list of lines or either a path to a json file'''
        __js_split__ = '';
        __lines__: list[str];
        if isinstance( obj, list ):
            __lines__ = obj;
        else:
            __lines__ = open( obj, 'r' ).readlines();
        for __line__ in __lines__:
            __line__ = __line__.strip();
            if __line__ and __line__ != '' and not __line__.startswith( '//' ):
                __js_split__ = f'{__js_split__}\n{__line__}';
        try:
            js = json.loads( __js_split__ );
            return js;
        except Exception as e:
            print( 'Failed to open object {}'.format( obj ) );
        return {};

    def to_command_choices( obj: dict[str, str] ) -> list[app_commands.Choice]:
        '''Converts a dictionary to a list of app_commands.Choice'''
        app_commands_choices = []
        for k, v in obj.items():
            app_commands_choices.append( app_commands.Choice( name=k, value=v ) );
        return app_commands_choices;

    def emote_number( number : str | int = None ) -> str | dict:
        '''
        return a number name equivalent to a emoji from a literal number

        if ``number`` is not provided then the dict is returned
        '''

        numbers = {
            '0': 'zero',
            '1': 'one',
            '2': 'two',
            '3': 'three',
            '4': 'four',
            '5': 'five',
            '6': 'six',
            '7': 'seven',
            '8': 'eight',
            '9': 'nine'
        };

        return numbers if number is None else ':' + numbers[ number if isinstance( number, str ) else str( number ) ] + ':';

# https://github.com/Rapptz/discord.py/blob/master/examples/app_commands/basic.py
class Bot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):

        if gpGlobals.workflow():
            return;
    
        if gpGlobals.developer():
            __MY_GUILD__ = discord.Object( id = self.LP() );
            self.tree.clear_commands(guild=__MY_GUILD__)
            self.tree.copy_global_to(guild=__MY_GUILD__)
            await self.tree.sync(guild=__MY_GUILD__)
        else:
            await self.tree.sync()

    def LP( self ) -> int:
        '''Limitless Potential server ID'''
        return 744769532513615922;

    async def log_channel( self, message: str, arguments: list = [] ):
        '''Log to #bots-testing channel'''
        for __arg__ in arguments:
            message = message.replace( "{}", str( __arg__ ), 1 )

        if gpGlobals.workflow():
            print( message );
            await self.get_channel( 1065791552485605446 ).send( message );
        else:
            await self.get_channel( 1211204941490688030 ).send( message );

    __pre_logs__:list[dict] = [];

    def pre_log_channel( self, message: str, arguments: list = [] ):
        '''Delay logs using this because the bot is not yet connected'''
        for __arg__ in arguments:
            message = message.replace( "{}", str( __arg__ ), 1 )
        self.__pre_logs__.append( message );

    async def hook_on_message( self, message: discord.Message ):
        '''on_message-based hooks'''

        # on_mention
        if message.mentions and len( message.mentions ) > 0:
            await g_PluginManager.CallHook( "on_mention", message, message.mentions );

        # on_reply
        if message.reference and message.reference.message_id:
            try:
                replied_message = await message.channel.fetch_message( message.reference.message_id );
                if replied_message:
                    await g_PluginManager.CallHook( "on_reply", message, replied_message );
            except discord.NotFound:
                pass;

        # on_link
        if 'https://' in message.content or 'www.' in message.content:
            contents = message.content.split();
            urls=[]
            for c in contents:
                if c.startswith( 'https://' ) or c.startswith( 'www.' ):
                    urls.append( c );
            if len( urls ) > 0:
                await g_PluginManager.CallHook( "on_link", message, urls );

    __fl_on_daily__ = 0;

    async def hook_on_think( self ):
        '''on_think-based hooks'''

        bldaily, self.__fl_on_daily__ = gpGlobals.should_think( self.__fl_on_daily__, 3600 );
        if bldaily:
            cache = gpUtils.jsonc( '{}cache.json'.format( gpGlobals.abs() ) );
            date = datetime.now();
            if date.day != cache[ "current.day" ]:
                await g_PluginManager.CallHook( "on_daily" );
                cache[ "current.day" ] = date.day;
                open( '{}cache.json'.format( gpGlobals.abs() ), 'w' ).write( json.dumps( cache, indent=0 ) );

    async def post_log_channel( self, num_plugins ):
        string = '';
        while len( self.__pre_logs__ ) > 0:
            if len( string ) + len( self.__pre_logs__[0] ) + 2 <= 2000: # Discord limit
                string = '{}{}\n'.format( string, self.__pre_logs__[0] );
                self.__pre_logs__.pop( 0 );
            else:
                await self.log_channel( string );
                string = '';
        if string != '':
            await self.log_channel( string );

        i = num_plugins;
        await bot.log_channel( '{} plugin{} were loaded'.format( 'No' if i <= 0 else 'One' if i == 1 else i, 's' if i > 1 else '' ) );

        await bot.log_channel( 'Bot connected and logged as {0.user}{1}'.format( bot, " in developer mode" if gpGlobals.developer() else '' ) )

global bot
bot: discord.Client | Bot = Bot(intents=discord.Intents.all())

class Hook:
    @staticmethod
    def Handled():
        '''Handles the hook and stop calling other plugins'''
        return 1;
    @staticmethod
    def Continue():
        '''Continue calling other hooks'''
        return 0;

class CPluginManager:

    def plugin_name( self, plugin: dict ) -> str:
        '''Return the plugin name if any, else is the name of the file'''
        return plugin[ "Plugin Name" ] if "Plugin Name" in plugin else plugin[ "File Name" ];

    __PluginsLoaded__ = 0;
    def num_plugins( self ) -> int:
        '''Return the number of loaded plugins'''
        return self.__PluginsLoaded__;

    __PluginsData__ = {}
    __PluginsNames__ = {}

    fnMethods = {};

    def fnMethodsInit( self ):
        try:
            Schema = gpUtils.jsonc( '{}schema.json'.format( gpGlobals.abs() ) );
            Enums = Schema["properties"]["plugins"]["items"]["properties"]["Hooks"]["items"]["enum"];
            for hook in Enums:
                self.fnMethods[ hook ] = [];
            if gpGlobals.workflow():
                bot.pre_log_channel( "Registered Schemas ```json\n{}```".format( json.dumps( Enums, indent=0 ).replace( '"on_', '"' ) ) );
        except Exception as e:
            print( "Failed to load plugin schema: {}".format( e ) );
            exit(1);

    def __init__( self ):

        self.fnMethodsInit();

        PluginObject = gpUtils.jsonc( '{}plugins.json'.format( gpGlobals.abs() ) );
        PluginData = PluginObject[ "plugins" ];

        for plugin in PluginData:

            if not "Author Name" in plugin:
                plugin[ "Author Name" ] = "Mikk"
            if not "Author Contact" in plugin:
                plugin[ "Author Contact" ] = "https://github.com/Mikk155/"

            if not plugin[ "Enable" ]:
                if not gpGlobals.developer():
                    bot.pre_log_channel( "Skipping disabled plugin \"{}\"".format( self.plugin_name( plugin ) ))
                continue;

            try:

                modulo:str = plugin[ "File Name" ][ : len(plugin[ "File Name" ]) - 3 ];

                spec = importlib.util.spec_from_file_location( modulo, '{}{}'.format( gpGlobals.absp(), plugin[ "File Name" ] ) );

                obj = importlib.util.module_from_spec( spec );

                spec.loader.exec_module( obj );

                self.module_cache[modulo] = obj

                self.__PluginsLoaded__ += 1;

                msg = 'Registered plugin **{}**'.format( modulo );

                if "Hooks" in plugin and len( plugin[ "Hooks" ] ) > 0:

                    msg += ' Using hooks ``{}``'.format( plugin[ "Hooks" ] );

                    for hook in plugin[ "Hooks" ]:

                        if hook in self.fnMethods:
                            self.fnMethods[ hook ].append( modulo );
                        else:
                            bot.pre_log_channel( "Undefined ``CPluginManager.fnMethods[ {} ]``".format( hook ) );

                if not gpGlobals.developer() and not gpGlobals.workflow():
                    bot.pre_log_channel( msg );

            except Exception as e:

                bot.pre_log_channel( "Error importing plugin {}: ``{}``", [ plugin[ "File Name" ], e ] );


            self.__PluginsData__[ modulo ] = plugin
            self.__PluginsNames__[ plugin[ "File Name" ] ] = modulo;

    module_cache = {}

    async def CallHook( self, hook_name, g1 = None, g2 = None, g3 = None ):

        for plugin in self.fnMethods[ hook_name ]:

            try:

                module = self.module_cache[ plugin ];
                hook = getattr( module, hook_name );

                hook_code: int;

                if g3 is not None:
                    hook_code = await hook( g1, g2, g3 );
                elif g2 is not None:
                    hook_code = await hook( g1, g2 );
                elif g1 is not None:
                    hook_code = await hook( g1 );
                else:
                    hook_code = await hook();

                # Don't call any more hooks
                if hook_code == Hook.Handled():
                    break;

            except Exception as e:

                str_except = 'Exception on plugin ``{}`` at function ``{}`` error: ```{}```'.format( plugin, hook_name, e );

                if str(e).find( 'has no attribute' ) != -1:
                    self.module_cache.pop( plugin );
                    str_except = "{}\nRemoving ``CPluginManager.module_cache[ {} ]`` to prevent recursion.".format( str_except, plugin );

                await bot.log_channel( str_except );

global g_PluginManager;
g_PluginManager = CPluginManager();

@bot.tree.command()
@app_commands.describe( plugin='Plugin' )
@app_commands.choices( plugin = gpUtils.to_command_choices( g_PluginManager.__PluginsNames__ ) )
async def plugin_info( interaction: discord.Interaction, plugin: app_commands.Choice[str] ):
    """Show plugins information"""
    try:
        info = g_PluginManager.__PluginsData__[ plugin.value ];

        msg = 'Plugin: ``{}``\n'.format( info[ "File Name" ] )
        msg += 'Active: ``{}``\n'.format( '✅' if info[ "Enable" ] else '❌' );
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
