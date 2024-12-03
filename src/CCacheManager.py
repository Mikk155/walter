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

class g_Cache:
    
    '''
    Cache System
    '''

    from src.CLogger import CLogger
    m_Logger = CLogger( "Cache System" );

    __cache__: dict = {};
    '''The whole cache (Do NOT modify directly! use g_Cache.get())'''

    @staticmethod
    def initialize() -> None:

        from src.utils.Path import g_Path;
        from src.utils.CJsonCommentary import jsonc;
        from os.path import exists;

        __cache_dir__ = g_Path.join( "cache.json" );

        if not exists(__cache_dir__ ):

            open( __cache_dir__, 'w' ).write( '{\n}' )

        cache = jsonc.load( g_Path.join( "cache.json" ) )

        from src.constdef import DEVELOPER;

        if not DEVELOPER():

            g_Cache.m_Logger.info(
                "object.initialized",
                [
                    __name__
                ],
                dev=True
            );

    class CCacheDictionary( dict ):

        def update( self, custom = None ):

            '''
            Update value to the cache\n
            This is only necesary when using self.pop or something else than indexing-value-set (__setitem__)
            '''

            from inspect import stack;
            from json import dumps;

            frame = stack()[1]; # Get caller plugin name

            n = custom.filename if custom else frame.filename;

            for s in [ '\\', '/' ]:

                if s in n:

                    n = n[ n.rfind( s ) + 1 if n.rfind( s ) != -1 else 0 : len( n ) ];

            if n in [ 'main.py', 'bot.py' ]:

                n = '__main__';


            from src.CConfigSystem import g_Config;

            # if "trace" in g_Config.configuration.get( "loggers", [] ):

                # -TODO Trace cache changes appropaitely
                # g_Cache.m_Logger.trace(
                #     "cache.update.pair",
                #     [
                #         n, dumps( g_Cache.__cache__.get( n, {} ) ), dumps( self )
                #     ],
                #     dev=True
                # );

            g_Cache.__cache__[ n ] = self; # Update cache context

            try: # Store cache context

                obj = dumps( g_Cache.__cache__, indent=4 );

                if obj:

                    from src.utils.Path import g_Path;

                    open( g_Path.join( "cache.json" ), 'w' ).write( obj );

                else:

                    raise Exception( "Failed to store cache." );

            except: # There's nothing to do so pass.

                pass;

        def __setitem__(self, key, value):

            super().__setitem__( key, value );

            from inspect import stack;

            self.update( stack()[1] );

    @staticmethod
    def get() -> CCacheDictionary:

        '''
        Return a dict which automatically stores into the cache.json when setting variables to it
        '''

        from inspect import stack;

        frame = stack()[1]; # Get caller plugin name

        n = frame.filename;

        for s in [ '\\', '/' ]:

            if s in n:

                n = n[ n.rfind( s ) + 1 if n.rfind( s ) != -1 else 0 : len( n ) ];

        if n in [ 'main.py', 'bot.py' ]:

            n = '__main__';

        return g_Cache.CCacheDictionary( g_Cache.__cache__.get( n,  { } ) );
