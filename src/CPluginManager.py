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

class Hooks:
    on_start = 'on_start';
    '''
    This is called only *once* at ``on_ready``

    Use this for initialization
    '''

    on_ready = 'on_ready';
    '''
    Called when the client is done preparing the data received from Discord.

    Usually after login is successful and the Client.guilds and co. are filled up.

    This function is not guaranteed to be the first event called. Likewise, this function is not guaranteed to only be called once.

    This library implements reconnection logic and thus will end up calling this event whenever a RESUME request fails.
    '''

    on_member_join = 'on_member_join';
    '''
    Called when a Member joins a Guild.
    '''

    on_member_remove = 'on_member_remove';
    '''
    Called when a Member leaves a Guild.
    '''

    on_message = 'on_message';
    '''
    Called when a Message is created and sent.

    The bot’s own messages messages are hooked through this event too.
    '''

    on_message_delete = 'on_message_delete';
    '''
    Called when a message is deleted.
    '''

    on_message_edit = 'on_message_edit';
    '''
    Called when a Message is edited.
    '''

    on_reaction_add = 'on_reaction_add';
    '''
    Called when a Reaction is added.
    '''

    on_reaction_remove = 'on_reaction_remove';
    '''
    Called when a Reaction is removed.
    '''

    on_think = 'on_think';
    '''
    Called every 1 second

    **NOTE**: This is not warantered to be a definitive value, the bot may delay by other operations.
    '''

    on_think_minute = 'on_think_minute';
    '''
    Called every 1 minute

    **NOTE**: This is not warantered to be a definitive value, the bot may delay by other operations.
    '''

    on_think_hour = 'on_think_hour';
    '''
    Called every 1 hour

    **NOTE**: This is not warantered to be a definitive value, the bot may delay by other operations.
    '''

    on_think_day = 'on_think_day';
    '''
    Called every 1 day

    **NOTE**: Unlikely other think functions, this is called individualy for each server when the timezone for that server matchs a new day

    **NOTE**: This is not warantered to be a definitive value, the bot may delay by other operations.
    '''

    on_mention = 'on_mention';
    '''
    Called when a user is mentioned in a Message.

    **NOTE**: this inherits from on_message and will call on_message after this method.
    '''

    on_reply = 'on_reply';
    '''
    Called when a user Message is a reply from another Message.

    **NOTE**: this inherits from on_message and will call on_message after this method.
    '''

    on_link = 'on_link';
    '''
    Called when Message contents a link.

    **NOTE**: this inherits from on_message and will call on_message after this method.
    '''

    on_typing = 'on_typing';
    '''
    Called when someone begins typing a message.

    The channel parameter could either be TextChannel, GroupChannel, or DMChannel.

    If the channel is a TextChannel then the user parameter is a Member, otherwise it is a User.
    '''

    # on_error = 'on_error';
    # on_command_error = 'on_command_error';
    # on_private_message = 'on_private_message';
    # on_reaction_clear = 'on_reaction_clear';
    # on_raw_reaction_add = 'on_raw_reaction_add';
    # on_raw_reaction_remove = 'on_raw_reaction_remove';
    # on_voice_state_update = 'on_voice_state_update';
    # on_member_update = 'on_member_update';
    # on_presence_update = 'on_presence_update';
    # on_connect = 'on_connect';
    # on_disconnect = 'on_disconnect';
    # on_resumed = 'on_resumed';
    # on_guild_emojis_update = 'on_guild_emojis_update';
    # on_guild_stickers_update = 'on_guild_stickers_update';
    # on_audit_log_entry_create = 'on_audit_log_entry_create';
    # on_invite_create = 'on_invite_create';
    # on_user_update = 'on_user_update';
    # on_poll_vote_add = 'on_poll_vote_add';
    # on_poll_vote_remove = 'on_poll_vote_remove';

class Command():
    '''Commands creation class'''

class Plugin():
    '''Define a plugin'''

    hooks: list[Hooks] = []
    '''List of plugin's Hooks, see ``Hooks`` class'''

    author: str = "Mikk"
    '''Name of the plugin's author'''

    contact: str = "https://github.com/Mikk155/"
    '''Contact info of the plugin's author'''

    name: str
    '''Name of the plugin, if empty the plugin's file name will be used'''

    servers: list[int] = []
    '''
    List of guild's ID that this plugin is only enabled for

    Leave empty to not delimit to any
    '''

    commands: list[Command]
    '''List of plugin's Commands, see ``Command`` class'''

    def __init__( self, name ):

        self.name = name;

class g_PluginManager:

    '''
    Plugin Manager System
    '''

    from datetime import datetime
    on_time_minute: datetime
    on_time_hour: datetime
    on_time_day: int
    on_time_listday: dict[str, int]

    from src.CLogger import CLogger
    m_Logger = CLogger( "Plugin Manager" );

    plugins: dict = {};
    '''Loaded plugins'''

    loaded: int = 0;
    '''Loaded plugins'''

    fnMethods: dict[str, list[str]] = {
        value: [] for name, value in vars(Hooks).items() if not name.startswith("__") and isinstance(value, str)
    };

    @staticmethod
    def install_requirements( requirements: str, plugin:str ) -> None:

        '''
        Install requirements
        '''

        from sys import executable;
        from subprocess import check_call, CalledProcessError;

        try:

            check_call( [ executable, "-m", "pip", "install", "-r", requirements ] );

            r = '';
            f = open( requirements, 'r' ).readlines();

            for l in f:
                r=f'{r}\n{l}';

            g_PluginManager.m_Logger.debug(
                "plugin_manager.requirements",
                [
                    plugin, r
                ],
                dev=True
            );

        except CalledProcessError as e:

            g_PluginManager.m_Logger.critical( e );

    module_cache: dict = {}

    @staticmethod
    def initialize() -> None:

        from json import dumps;
        from os.path import exists;
        from src.CConfigSystem import g_Config;
        from src.utils.Path import g_Path;
        from src.constdef import INVALID_INDEX, DEVELOPER;
        from src.CSentences import g_Sentences;
        from src.utils.format import g_Format;

        from datetime import datetime;
        g_PluginManager.on_time_minute = datetime.now();
        g_PluginManager.on_time_hour = datetime.now();
        g_PluginManager.on_time_day = datetime.now().day - 1;
        g_PluginManager.on_time_listday = {};

        from importlib import util as lib;

        for plugin in g_Config.plugins:

            if plugin.get( 'Disable', False ):

                if not DEVELOPER():

                    g_PluginManager.m_Logger.info(
                        "plugin_manager.disabled",
                        [
                            plugin[ "script" ]
                        ],
                        dev=True
                    );

                g_PluginManager.plugins[ plugin[ "script" ] ] = None;

                continue;

            try:

                modulo:str = plugin[ "script" ][ : len( plugin[ "script" ] ) - 3 ];

                pyfile = g_Path.join( f'plugins/{plugin[ "script" ]}' );

                if not exists( pyfile ):

                    not_exist_sentence = g_Sentences.get( "file_does_not_exists" );

                    not_exist_fmt = g_Format.brackets( not_exist_sentence, [ pyfile ] );

                    g_PluginManager.m_Logger.warn(
                        "plugin_manager.exception",
                        [
                            plugin[ "script" ],
                            not_exist_fmt
                        ],
                        dev=True
                    );

                    continue;

                if not DEVELOPER():

                    requirements = pyfile.replace( '.py', '_requirements.txt' );

                    if exists( requirements ):

                        g_PluginManager.install_requirements( requirements, plugin[ "script" ] );

                spec = lib.spec_from_file_location( modulo, pyfile );

                obj = lib.module_from_spec( spec );

                spec.loader.exec_module( obj );

                g_PluginManager.module_cache[modulo] = obj

                p_Plugin = Plugin( plugin[ "script" ] );

                p_Plugin: Plugin = obj.on_initialization( p_Plugin );

                if not DEVELOPER():

                    g_PluginManager.m_Logger.info(
                        "plugin_manager.register",
                        [
                            p_Plugin.name
                        ],
                        dev=True
                    );

                    g_PluginManager.m_Logger.trace( f"```json\n{dumps( p_Plugin, indent=1 )}```", dev=True );

                for hook in p_Plugin.hooks:

                    if hook in g_PluginManager.fnMethods:

                        fnMethod = g_PluginManager.fnMethods[ hook ];

                        fnMethod.append( modulo );

                        g_PluginManager.fnMethods[ hook ] = fnMethod;

                    else:

                        g_PluginManager.m_Logger.warn(
                            "plugin_manager.hook.undefined",
                            [
                                plugin[ "script" ],
                                hook
                            ],
                            dev=True
                        );

                g_PluginManager.plugins[ plugin[ "script" ] ] = p_Plugin;

                g_PluginManager.loaded += 1;

            except Exception as e:

                g_PluginManager.m_Logger.error(
                    "plugin_manager.exception",
                    [
                        plugin[ "script" ],
                        e
                    ],
                    dev=True
                );

        g_PluginManager.m_Logger.info( "object_initialized", [ __name__ ], dev=True );

        if not DEVELOPER():

            g_PluginManager.m_Logger.info(
                "Hooks:```json\n{}```",
                [
                    dumps(g_PluginManager.fnMethods, indent=2)
                ],
                dev=True
            );

    @staticmethod
    async def callhook( hook_name: str, g1 = None, g2 = None, g3 = None, guild=None ) -> None:
        '''
        Hook all functions with the given name
        '''

        from src.constdef import HOOK_HANDLED;

        for plugin in g_PluginManager.fnMethods[ hook_name ]:

            try:

                if not plugin in g_PluginManager.module_cache:
                    continue;

                __allowed_servers__ = g_PluginManager.plugins[ f'{plugin}.py' ].servers;

                if len( __allowed_servers__ ) > 0:
                    
                    if not guild or guild and not guild.id in __allowed_servers__:

                        continue;

                module = g_PluginManager.module_cache[ plugin ];

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
                if hook_code == HOOK_HANDLED():

                    break;

            except Exception as e:

                __attribute__ = ''

                if str(e).find( 'has no attribute' ) != -1:

                    g_PluginManager.module_cache.pop( plugin );

                    from src.CSentences import g_Sentences

                    __attribute__ = g_Sentences.get( 'plugin_manager.callhook.attribute' )

                g_PluginManager.m_Logger.error(
                    'plugin_manager.callhook.exception',
                    [
                        plugin,
                        hook_name,
                        e,
                        __attribute__
                    ],
                    dev=True
                );
