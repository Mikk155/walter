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
import io
import os
import re
import sys
import time
import json
import random
import asyncio
import inspect
import aiohttp
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

if not os.path.exists( '{}/cache.json'.format( os.path.abspath("") ) ):
    open( '{}/cache.json'.format( os.path.abspath("") ), 'w' ).write( '{\n}' )

#=======================================================================================
# Global Public variables
#=======================================================================================
global gpGlobals
class gpGlobals:
    '''Global variables'''

    @staticmethod
    def abs() -> str:
        '''Return absolute path value to the bot folder'''
        return os.path.abspath( "" );

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

        if var >= gpGlobals.time():
            return False, var;
        var = gpGlobals.time() + next_think;
        return True, var;

    class CCacheManager():

        __cache__: dict

        def __init__( self, obj ):
            self.__cache__ = obj;

        class CCacheDictionary( dict ):

            def update( self, custom = None ):
                '''
                Update value to the cache\n
                This is only necesary when using self.pop or something else than indexing-value-set (__setitem__)
                '''

                frame = inspect.stack()[1]; # Get caller plugin name

                n = custom.filename if custom else frame.filename;

                for s in [ '\\', '/' ]:
                    if s in n:
                        n = n[ n.rfind( s ) + 1 if n.rfind( s ) != -1 else 0 : len( n ) ];

                if n in [ 'main.py', 'bot.py' ]:
                    n = '__main__';

                gpGlobals.cache.__cache__[ n ] = self; # Update cache context

                try: # Store cache context
                    obj = json.dumps( gpGlobals.cache.__cache__, indent=4 );
                    if obj:
                        open( '{}/cache.json'.format( gpGlobals.abs() ), 'w' ).write( obj );
                    else:
                        raise Exception( "Failed to store cache." );
                except: # There's nothing to do so pass.
                    pass;

            def __setitem__(self, key, value):
                super().__setitem__( key, value );
                self.update( inspect.stack()[1] );

        def get( self ) -> CCacheDictionary:
            '''Return a dict which automatically stores into the cache.json when setting variables to it'''
            frame = inspect.stack()[1]; # Get caller plugin name
            n = frame.filename;
            for s in [ '\\', '/' ]:
                if s in n:
                    n = n[ n.rfind( s ) + 1 if n.rfind( s ) != -1 else 0 : len( n ) ];
            if n in [ 'main.py', 'bot.py' ]:
                n = '__main__';
            return self.CCacheDictionary( self.__cache__.get( n,  { } ) );

    
    cache = CCacheManager( json.load( open( '{}/cache.json'.format( os.path.abspath("") ), 'r' ) ) );
    '''Access to the bot cache'''

    class LimitlessPotential:
        '''Limitless Potential Server stuff'''

        server_id = 744769532513615922;
        '''Server ID'''

        github_id = 1065791552485605446;
        '''Github webhook channel ID'''

        log_id = 1211204941490688030;
        '''#bots-testing channel ID'''

        mikk_id = 744768007892500481;
        '''Owner ID, must have total authority over the bot code'''

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

    def mention( user: discord.Member ) -> str:
        '''
        Return a fixed ``discord.Member.mention`` string for globalization\n
        nsince a leading characters are added when the user has a nickname
        '''
        return f"<@{user.id}>"

    def get_time( seconds : int ) -> str:
        '''Get time in a ``hh:mm:ss`` format'''
        m = seconds // 60;
        sr = seconds % 60;
        return f"{m}m:{sr:02d}s";

    def jsonc( obj : list[str] | str ) -> dict | list:
        '''Open a json file ignoring single-line commentary\n
        Returns empty dict if an Exception is thrown\n
        **obj** list of lines or either a path to a json file\n
        This functions is delimited to the absolute path of the bot.py folder and subfolders'''
        __js_split__ = '';
        __lines__: list[str];
        if isinstance( obj, list ):
            __lines__ = obj;
        else:
            __lines__ = open( '{}/{}'.format( gpGlobals.abs(), obj ), 'r' ).readlines();
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

    def to_command_choices( obj: dict[str, str] | list[str] ) -> list[app_commands.Choice]:
        '''Converts a dictionary to a list of app_commands.Choice'''
        app_commands_choices = []
        if isinstance( obj, dict ):
            for k, v in obj.items():
                app_commands_choices.append( app_commands.Choice( name=k, value=v ) );
        else:
            for i, k in enumerate(obj):
                app_commands_choices.append( app_commands.Choice( name=k, value=str(i) ) );
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

#=======================================================================================
# Translations
#=======================================================================================
global sentences;
sentences = gpUtils.jsonc( 'sentences.json' )
def AllocString( message: str, arguments: list = [], server_id: int = None ):
    '''
    **message**: A dict name key located in sentences.json.

    **arguments**: Arguments to replace brackets in the messages.

    **server_id**: Server id so we pick the proper language.
    '''

    msg_dict = sentences.get( message, {} );

    cache = gpGlobals.cache.get();

    language = 'english';

    if str( server_id ) in cache:
        srvcache = cache[ str( server_id ) ];
        language = srvcache.get( 'language', 'english' );

    msg = '';

    if language in msg_dict:
        msg = msg_dict[ language ];
    else:
        msg = msg_dict[ 'english' ];

    for __arg__ in arguments:
        msg = msg.replace( "{}", str( __arg__ ), 1 );

    return msg;

# https://github.com/Rapptz/discord.py/blob/master/examples/app_commands/basic.py
class Bot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):

        if gpGlobals.workflow():
            return;

        if gpGlobals.developer():
            __MY_GUILD__ = discord.Object( id = gpGlobals.LimitlessPotential.server_id );
            self.tree.clear_commands(guild=__MY_GUILD__)
            self.tree.copy_global_to(guild=__MY_GUILD__)
            await self.tree.sync(guild=__MY_GUILD__)
        else:
            await self.tree.sync();

    async def log_channel( self, message: str, arguments: list = [] ):
        '''Log to #bots-testing channel'''
        for __arg__ in arguments:
            message = message.replace( "{}", str( __arg__ ), 1 )

        if gpGlobals.workflow():
            print( message );
            await self.get_channel( gpGlobals.LimitlessPotential.github_id ).send( message );
        else:
            await self.get_channel( gpGlobals.LimitlessPotential.log_id ).send( message );

    async def handle_exception( self, __type__: ( discord.Interaction | discord.Message ), exception = 'unknown', additional = {} ):
        '''
        Handles and log an Exception
        
        **__type__**: Instance to identify the exception, from which server, channel etc

        **exception**: Exception instance

        **additional**: Additional parameters to show to the developer
        '''
        try:
            if isinstance( __type__, discord.Interaction ) or isinstance( __type__, discord.TextChannel ):
                await __type__.channel.send( "Something went wrong, an Exception log has been submitted to my developers." );
                additional[ "server_id" ] = __type__.guild_id;
                if __type__.guild:
                    additional[ "server_name" ] = __type__.guild.name;
        except:
            pass;
        try:
            frame = inspect.stack()[1];

            message = '- ``[{}]`` **Exception:** ``{}`` from function ``{}``{}'.format(
                frame.filename[ frame.filename.rfind( '/' ) + 1 if frame.filename.rfind( '/' ) != -1 else 0 : len( frame.filename ) ],
                str(exception),
                frame.function,
                '\n```json\n{}```'.format( json.dumps( additional, indent=1 ) ) if len( additional ) > 0 else ''
            );

            await self.log_channel( message );
        except:
            pass;

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
            date = datetime.now();
            gdate = gpGlobals.cache.get();
            if date.day != gdate.get( "current.day", 0 ):
                await g_PluginManager.CallHook( "on_daily" );
                gdate[ "current.day" ] = date.day;

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
            Schema = gpUtils.jsonc( 'schema.json' );
            Enums = Schema["properties"]["plugins"]["items"]["properties"]["Hooks"]["items"]["enum"];
            for hook in Enums:
                self.fnMethods[ hook ] = [];
            if not gpGlobals.developer():
                bot.pre_log_channel( "Registered Schemas ```json\n{}```".format( json.dumps( Enums, indent=0 ).replace( '"on_', '"' ) ) );
        except Exception as e:
            print( "Failed to load plugin schema: {}".format( e ) );
            exit(1);

    def __init__( self ):

        self.fnMethodsInit();

        PluginObject = gpUtils.jsonc( 'plugins.json' );
        PluginData = PluginObject[ "plugins" ];

        for plugin in PluginData:

            if not "Author Name" in plugin:
                plugin[ "Author Name" ] = "Mikk"
            if not "Author Contact" in plugin:
                plugin[ "Author Contact" ] = "https://github.com/Mikk155/"

            if "Disable" in plugin and not plugin[ "Disable" ]:
                if not gpGlobals.developer():
                    bot.pre_log_channel( "Skipping disabled plugin \"{}\"".format( self.plugin_name( plugin ) ))
                continue;

            try:

                modulo:str = plugin[ "File Name" ][ : len(plugin[ "File Name" ]) - 3 ];

                spec = importlib.util.spec_from_file_location( modulo, '{}/plugins/{}'.format( gpGlobals.abs(), plugin[ "File Name" ] ) );

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

                if not plugin in self.module_cache:
                    continue;

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
