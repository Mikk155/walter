class g_Cache:
    
    '''
        Cache System
    '''

    from src.utils.Logger import Logger
    m_Logger = Logger( "Cache System" );

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

        from src.utils.CJsonCommentary import jsonc;
        from os.path import exists, join, abspath;

        __cache_dir__ = join( abspath(""), ( "cache.json" ) );

        if not exists(__cache_dir__ ):

            open( __cache_dir__, 'w' ).write( '{\n}' )

        __json__ = jsonc.load( __cache_dir__ )

        g_Cache.__cache__ = g_Cache.CCacheDictionary( __json__ );

    def __update__():

        from json import dumps;

        # -TODO g_Cache.m_Logger.trace changes

        try: # Store cache context

            obj = dumps( dict(g_Cache.__cache__), indent=4 );

            if obj:

                from os.path import join, abspath;
                open( join( abspath(""), ( "cache.json" ) ), 'w' ).write( obj );

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

        return g_Cache.__cache__[ label ];
