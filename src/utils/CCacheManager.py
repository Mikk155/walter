class g_Cache:
    
    '''
        Cache System
    '''

    from src.utils.Logger import Logger;
    m_Logger = Logger( "Cache System" );

    class CCacheDictionary( dict ):

        def __getitem__( self, key ):

            if key not in self:

                cache_dict = g_Cache.CCacheDictionary();

                self[ key ] = cache_dict;

                return cache_dict;

            return super().__getitem__( key );

        def __setitem__( self, key, value ):

            if isinstance( value, dict ):

                value = g_Cache.CCacheDictionary( value );

            super().__setitem__( key, value );

        def __repr__( self ):

            from json import dumps;

            __json__ = dumps( super().__repr__(), indent=4);

            return __json__;

    __cache__: CCacheDictionary = None;
    '''The whole cache (Do NOT modify directly! use g_Cache.get())'''

    @staticmethod
    def initialize() -> None:

        from src.utils.fmt import fmt;
        from src.utils.jsonc import jsonc;

        __json__ = jsonc.load( fmt.join( "cache.json" ), exists_ok=True );

        g_Cache.__cache__ = g_Cache.CCacheDictionary( __json__ );

    def __update__():

        from json import dumps;

        # -TODO g_Cache.m_Logger.trace changes

        try: # Store cache context

            obj = dumps( dict(g_Cache.__cache__), indent=4 );

            if obj:

                from src.utils.fmt import fmt;

                open( fmt.join( "cache.json" ), 'w' ).write( obj );

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

    @staticmethod
    def set( label: str, value ) -> None:

        g_Cache.__cache__[ label ] = value;

