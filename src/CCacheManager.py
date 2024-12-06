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

    class CCacheDictionary( dict ):

        def __getitem__( self, key ):

            if key not in self:

                self[ key ] = g_Cache.CCacheDictionary();

            return super().__getitem__( key );

        def __setitem__( self, key, value ):

            if isinstance( value, dict ):

                value = g_Cache.CCacheDictionary( value );

            super().__setitem__( key, value );

        def __repr__( self ):

            from json import dumps;

            __json__ = dumps( super().__repr__(), indent=4);

            return __json__;

    __cache__: CCacheDictionary = {};
    '''The whole cache (Do NOT modify directly! use g_Cache.get())'''

    @staticmethod
    def initialize() -> None:

        from src.utils.Path import g_Path;
        from src.utils.CJsonCommentary import jsonc;
        from os.path import exists;

        __cache_dir__ = g_Path.join( "cache.json" );

        if not exists(__cache_dir__ ):

            open( __cache_dir__, 'w' ).write( '{\n}' )

        __json__ = jsonc.load( g_Path.join( "cache.json" ) )

        g_Cache.__cache__ = g_Cache.CCacheDictionary( __json__ );

        from src.constdef import DEVELOPER;

        if not DEVELOPER():

            g_Cache.m_Logger.info(
                "object.initialized",
                [
                    __name__
                ],
                dev=True
            );

    def __update__():

        from json import dumps;

        # -TODO g_Cache.m_Logger.trace changes

        try: # Store cache context

            from src.CConfigSystem import g_Config;

            obj = dumps( dict(g_Cache.__cache__), indent=4 );

            if obj:

                from src.utils.Path import g_Path;

                open( g_Path.join( "cache.json" ), 'w' ).write( obj );

            else:

                raise Exception( "Failed to store cache." );

        except Exception as e:

            print( e );

            pass;

    @staticmethod
    def get( label: str = None ) -> CCacheDictionary:

        '''
        Return a dict which automatically stores into the cache.json when setting variables to it
        '''

        n = ''

        if label:

            n = label;

        else:

            from inspect import stack;

            frame = stack()[1]; # Get caller plugin name

            n = frame.filename;

            for s in [ '\\', '/' ]:

                if s in n:

                    n = n[ n.rfind( s ) + 1 if n.rfind( s ) != -1 else 0 : len( n ) ];

            if n.startswith( "src." ) or n == 'bot.py':

                n = '__main__';

        return g_Cache.__cache__[ n ];
