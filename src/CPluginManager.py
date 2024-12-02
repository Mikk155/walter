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
    on_initialization = 'on_initialization';

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
        Hooks.on_initialization: [],
    };

    @staticmethod
    def install_requirements( requirements: str ) -> None:

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

            __Logger__ = {
                "arguments": [ r ],
                "print dev": True,
            };

            g_PluginManager.m_Logger.info( "plugin.manager.requirements", __Logger__ );

        except CalledProcessError as e:

            g_PluginManager.m_Logger.error( e );

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

                __Logger__ = {
                    "arguments": [ plugin[ "script" ] ],
                    "print dev": True
                };

                g_PluginManager.m_Logger.info( "plugin.manager.disabled", __Logger__ );

                continue;

            try:

                modulo:str = plugin[ "script" ][ : len( plugin[ "script" ] ) - 3 ];

                pyfile = g_Path.join( f'plugins/{plugin[ "script" ]}' );

                if not exists( pyfile ):

                    not_exist_sentence = g_Sentences.get( "file.not.exists" );

                    not_exist_fmt = g_Format.brackets( not_exist_sentence, [ pyfile ] );

                    __Logger__ = {
                        "arguments": [ plugin[ "script" ], not_exist_fmt ],
                        "print dev": True,
                    };

                    g_PluginManager.m_Logger.warn( "plugin.manager.exception", __Logger__ );

                    continue;

                requirements = pyfile.replace( '.py', '.txt' );

                if exists( requirements ):

                    g_PluginManager.install_requirements( requirements );

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

                __Logger__ = {
                    "arguments": [ plugin_data[ "name" ] ],
                    "print console": True,
                    "print dev": True,
                };

                g_PluginManager.m_Logger.info( "plugin.manager.register", __Logger__ );

                g_PluginManager.m_Logger.debug( f"```json\n{dumps( plugin_data, indent=1 )}```" );

                for hook in plugin_data.get( "hooks", [] ):

                    if hook in g_PluginManager.fnMethods:

                        fnMethod = g_PluginManager.fnMethods[ hook ];

                        fnMethod.append( modulo );

                        g_PluginManager.fnMethods[ hook ] = fnMethod;

                    else:

                        __Logger__ = {
                            "arguments": [ plugin[ "script" ], hook ],
                            "print dev": True,
                        };

                        g_PluginManager.m_Logger.warn( "plugin.manager.hook.undefined", __Logger__ );

                g_PluginManager.plugins[ plugin[ "script" ] ] = plugin_data;

                g_PluginManager.loaded += 1;

            except Exception as e:

                __Logger__ = {
                    "arguments": [ plugin[ "script" ], e ],
                    "print dev": True,
                };

                g_PluginManager.m_Logger.error( "plugin.manager.exception", __Logger__ );

        g_PluginManager.m_Logger.info( "object.initialized", { "arguments": [ __name__ ], "print dev": True, } );
