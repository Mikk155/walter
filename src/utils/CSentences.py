class sentence( dict ):

    '''
        Bot Sentences
    '''

    from src.utils.Logger import Logger
    m_Logger = Logger( "Sentences" );

    def __init__( self ):

        from src.utils.CJsonCommentary import jsonc;
        from os.path import exists, join, abspath;

        __sentences_dir__ = join( join( abspath(""), "src" ), "sentences.json" );

        if not exists(__sentences_dir__ ):

            open( __sentences_dir__, 'w' ).write( '{\n}' )

        super().__init__( jsonc.load( __sentences_dir__ ) );

    def get( self, key: str, *args ) -> str:

        __sentence__: str = None;

        if key in self:

            __sslot__ = super().get( key, {} );

            if "english" in __sslot__:

                __sentence__ = __sslot__[ "english" ];

            else:

                self.m_Logger.critical( "Failed to get language {} for sentence {}", "english", key )

        else:

            self.m_Logger.error( "Undefined sentence {}", key )

        if __sentence__ is None:

            return f"Trans#{key}";

        for arg in args:

            if not '{}' in __sentence__:
                break;

            __sentence__ = __sentence__.replace( "{}", arg if isinstance( arg, str ) else str(arg), 1 );

        return __sentence__;
