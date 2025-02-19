class sentence( dict ):

    '''
        Bot Sentences
    '''

    from src.utils.Logger import Logger
    m_Logger = Logger( "Sentences" );

    def __init__( self ):

        from mikk import jsonc, fmt;
        from os.path import exists, join, abspath;
        super().__init__( jsonc.load( fmt.join("src/sentences.json" ) ) );

    def get( self, key: str, *args ) -> str:

        __sentence__: str = None;

        if key in self:

            __sslot__ = super().get( key, {} );

            if "english" in __sslot__:

                __sentence__ = __sslot__[ "english" ];

            else:

                self.m_Logger.critical( "Failed to get language {} for sentence {}", "english", key ).print()

        else:

            self.m_Logger.error( "Undefined sentence {}", key ).print()

        if __sentence__ is None:

            return f"Trans#{key}";

        for arg in args:

            if not '{}' in __sentence__:
                break;

            __sentence__ = __sentence__.replace( "{}", arg if isinstance( arg, str ) else str(arg), 1 );

        return __sentence__;
