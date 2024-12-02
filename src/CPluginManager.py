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

    on_embeed = 'on_embeed';
    '''
	Called when Message contents a embeed.

    **NOTE**: this inherits from on_message and will call on_message after this method.
    '''

    on_daily = 'on_daily';
    '''
	Called every day
    '''

    on_typing = 'on_typing';
    on_error = 'on_error';
    on_command_error = 'on_command_error';
    on_private_message = 'on_private_message';
    on_reaction_clear = 'on_reaction_clear';
    on_raw_reaction_add = 'on_raw_reaction_add';
    on_raw_reaction_remove = 'on_raw_reaction_remove';
    on_voice_state_update = 'on_voice_state_update';
    on_member_update = 'on_member_update';
    on_presence_update = 'on_presence_update';
    on_connect = 'on_connect';
    on_disconnect = 'on_disconnect';
    on_resumed = 'on_resumed';
    on_guild_emojis_update = 'on_guild_emojis_update';
    on_guild_stickers_update = 'on_guild_stickers_update';
    on_audit_log_entry_create = 'on_audit_log_entry_create';
    on_invite_create = 'on_invite_create';
    on_user_update = 'on_user_update';
    on_poll_vote_add = 'on_poll_vote_add';
    on_poll_vote_remove = 'on_poll_vote_remove';

fnMethods: dict[str, list[str]] = {
    value: [] for name, value in vars(Hooks).items() if not name.startswith("__") and isinstance(value, str)
};
import json
print( json.dumps(fnMethods, indent=2))
exit(0)
class g_PluginManager:
    
    '''
    Plugin Manager System
    '''

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
                "plugin.manager.requirements",
                [
                    plugin.replace( '.py', '.txt' ), r
                ],
                dev=True
            );

        except CalledProcessError as e:

            g_PluginManager.m_Logger.critical( e );

    @staticmethod
    def initialize() -> None:

        from json import dumps;
        from os.path import exists;
        from src.CConfigSystem import g_Config;
        from src.utils.Path import g_Path;
        from src.constdef import INVALID_INDEX;
        from src.CSentences import g_Sentences;
        from src.utils.format import g_Format;

        from importlib import util as lib;

        for plugin in g_Config.plugins:

            if plugin.get( 'Disable', False ):

                g_PluginManager.m_Logger.info(
                    "plugin.manager.disabled",
                    [
                        plugin[ "script" ]
                    ],
                    dev=True
                );

                continue;

            try:

                modulo:str = plugin[ "script" ][ : len( plugin[ "script" ] ) - 3 ];

                pyfile = g_Path.join( f'plugins/{plugin[ "script" ]}' );

                if not exists( pyfile ):

                    not_exist_sentence = g_Sentences.get( "file.not.exists" );

                    not_exist_fmt = g_Format.brackets( not_exist_sentence, [ pyfile ] );

                    g_PluginManager.m_Logger.warn(
                        "plugin.manager.exception",
                        [
                            plugin[ "script" ],
                            not_exist_fmt
                        ],
                        dev=True
                    );

                    continue;

                requirements = pyfile.replace( '.py', '.txt' );

                if exists( requirements ):

                    g_PluginManager.install_requirements( requirements, plugin[ "script" ] );

                spec = lib.spec_from_file_location( modulo, pyfile );

                obj = lib.module_from_spec( spec );

                spec.loader.exec_module( obj );

                plugin_data = obj.on_initialization();

                if not "author" in plugin_data:

                    plugin_data[ "author" ] = "Mikk";

                if not "contact" in plugin:

                    plugin_data[ "contact" ] = "https://github.com/Mikk155/";

                if not "name" in plugin_data:

                    plugin_data[ "name" ] = plugin[ "script" ];

                g_PluginManager.m_Logger.info(
                    "plugin.manager.register",
                    [
                        plugin_data[ "name" ]
                    ],
                    dev=True
                );

                g_PluginManager.m_Logger.debug( f"```json\n{dumps( plugin_data, indent=1 )}```" );

                for hook in plugin_data.get( "hooks", [] ):

                    if hook in g_PluginManager.fnMethods:

                        fnMethod = g_PluginManager.fnMethods[ hook ];

                        fnMethod.append( modulo );

                        g_PluginManager.fnMethods[ hook ] = fnMethod;

                    else:

                        g_PluginManager.m_Logger.warn(
                            "plugin.manager.hook.undefined",
                            [
                                plugin[ "script" ],
                                hook
                            ],
                            dev=True
                        );

                g_PluginManager.plugins[ plugin[ "script" ] ] = plugin_data;

                g_PluginManager.loaded += 1;

            except Exception as e:

                g_PluginManager.m_Logger.error(
                    "plugin.manager.exception",
                    [
                        plugin[ "script" ],
                        e
                    ],
                    dev=True
                );

        g_PluginManager.m_Logger.info(
            "object.initialized",
            [
                __name__
            ],
            dev=True
        );
