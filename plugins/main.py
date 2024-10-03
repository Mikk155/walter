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
from discord import app_commands
from discord.ext import commands, tasks
from bs4 import BeautifulSoup

global gpGlobals
class gpGlobals:

    time = 0;
    '''Current time of think.
    This increases in 1 each second.
    '''

    developer = True if '-dev' in sys.argv else False;
    '''
    Returns **True** If the bot has been run by ``test.bat``
    '''

    Logger = True
    '''
    Set to *True* for getting loggers
    '''

    __iPlugins__ = 0;

async def log_channel( message: str, arguments: list = [] ):
    global config;
    if gpGlobals.Logger:
        for __arg__ in arguments:
            message = message.replace( "{}", str( __arg__ ), 1 )
        return await bot.get_channel( 1211204941490688030 ).send( message );

global __pre_logs__;
__pre_logs__:list[dict] = []

def pre_log_channel( message: str, arguments: list = [] ):
    '''Delay logs using this because the bot is not yet connected'''
    for __arg__ in arguments:
        message = message.replace( "{}", str( __arg__ ), 1 )
    global __pre_logs__;
    __pre_logs__.append( message );

async def post_log_channel():
    global __pre_logs__;
    string = '';
    while len( __pre_logs__ ) > 0:
        if len( string ) + len( __pre_logs__[0] ) + 2 <= 2000: # Discord limit
            string = '{}{}\n'.format( string, __pre_logs__[0] );
            __pre_logs__.pop( 0 );
        else:
            await log_channel( string );
            string = '';
    if string != '':
        await log_channel( string );
        

def get_time( seconds : int ) -> str:
    m = seconds // 60;
    sr = seconds % 60;
    return f"{m}m:{sr:02d}s";

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

def jsonc( obj : list[str] | str ) -> dict | list:
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

global abspath;
abspath = os.path.abspath( "" );

global config
config:dict = jsonc( '{}\\config.json'.format( abspath ) );

if not config:
    raise Exception( 'Can not open config.json!' )

global __LP__;
__LP__ = 744769532513615922;

# https://github.com/Rapptz/discord.py/blob/master/examples/app_commands/basic.py
class Bot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        if gpGlobals.developer:
            __MY_GUILD__ = discord.Object(id=__LP__)
            self.tree.clear_commands(guild=__MY_GUILD__)
            self.tree.copy_global_to(guild=__MY_GUILD__)
            await self.tree.sync(guild=__MY_GUILD__)
        else:
            await self.tree.sync()

global bot
bot: discord.Client = Bot(intents=discord.Intents.all())

global modulos;
plugins : dict = {};

class ReturnCode:
    Handled = 1;
    '''Handles the hook and stop calling other plugins'''
    Continue = 0;
    '''Continue calling other hooks'''

class Hooks:
    '''
    Hooks supported for the bot
    '''
    on_ready = 'on_ready'
    on_think = 'on_think'
    on_member_join = 'on_member_join'
    on_member_remove = 'on_member_remove'
    on_message = 'on_message'
    on_message_delete = 'on_message_delete'
    on_message_edit = 'on_message_edit'
    on_reaction_add = 'on_reaction_add'
    on_reaction_remove = 'on_reaction_remove'

def RegisterHooks( plugin_name : str, hook_list : list[ Hooks ] ):

    if plugin_name.endswith( '.py' ):
        plugin_name = plugin_name[ : len( plugin_name ) - 3 ]
        if plugin_name.find( '\\' ) != -1:
            plugin_name = plugin_name[ plugin_name.rfind( '\\' ) + 1 : ];

    plugins[ plugin_name ] =  hook_list;
    pre_log_channel( '**{}** Registered hooks: ``{}``', [ plugin_name, hook_list ] );

class HookValue:
    class edited:
        before : discord.Message
        after : discord.Message
    class reaction:
        reaction : discord.Reaction
        user : discord.User

class HookManager:

    module_cache = {}

    @classmethod
    async def CallHook( self, hook_name, HookValues = None ):

        for plugin, hooks in plugins.items():

            if f'{hook_name}' in hooks:

                try:

                    module = self.module_cache[ plugin ];
                    hook = getattr( module, hook_name );

                    hook_code = await hook( HookValues ) if HookValues is not None else await hook();

                    # Don't call anymore hooks
                    if hook_code == ReturnCode.Handled:
                        break;

                except Exception as e:

                    str_except = 'Exception on plugin ``{}`` at function ``{}`` error: ```{}```'.format( plugin, hook_name, e );

                    if HookValues:
                        if isinstance( HookValues, discord.Message ) or isinstance( HookValues, HookValue.edited ):
                            try:
                                await HookValues.channel.send( str_except );
                            except:
                                await log_channel( str_except );
                        elif isinstance( HookValues, HookValue.reaction ):
                            try:
                                await HookValues.message.channel.send( str_except );
                            except:
                                await log_channel( str_except );
                    else:
                        await log_channel( str_except );
