class CSentences( dict ):

    '''
        Sentences
    '''

    def __init__( self ):

        from mikk import jsonc, fmt;
        super().__init__( jsonc.load( fmt.join("src/sentences.json" ) ) );
        from src.utils.Logger import Logger;
        self.m_Logger = Logger( "Sentences" );

    def __getitem__( self, message: str ) -> str:

        if message in self:

            slot = super().get( message, {} );

            if "english" in slot:

                return slot[ "english" ];

            else:

                self.m_Logger.critical( "Undefined language {} for sentence {}", "english", message ).print();

        else:

            self.m_Logger.critical( "Undefined sentence {}", message ).print();

        return f"Trans#{message}";

global sentences;
sentences: CSentences = CSentences();
