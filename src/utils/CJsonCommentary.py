class jsonc:

    from src.utils.Logger import Logger;
    m_Logger = Logger( "Json" );

    @staticmethod
    def load( object: str, exists_ok = False ) -> dict | list:

        '''
        Open a json file ignoring single-line commentary

        Returns empty dict if an Exception is thrown

        **object** Path to a json file or a string with json format

        **exists_ok** If true when the file doesn't exist we create it and return a empty dict instead of throwing a warning error
        '''

        filenm = None

        if object.endswith( '.json' ):

            filenm = object;

            from os.path import exists;

            if exists( object ):

                with open( file = object, mode = 'r', encoding = 'utf-8' ) as __file__:
        
                    object = __file__.readlines();

            elif exists_ok:

                open( object, 'w' ).write( "{\n}" );

                return {};

            else:

                jsonc.m_Logger.error( "File \"{}\" Doesn't exists", object );

                return {};

        from json import loads

        __js_split__ = '';

        if isinstance( object, str ):

            __js_split__ = object;
        
        else:

            for __line__ in object:

                __line__ = __line__.strip();

                if __line__ and __line__ != '' and not __line__.startswith( '//' ):

                    __js_split__ = f'{__js_split__}\n{__line__}';

        try:

            js = loads( __js_split__ );

            return js;

        except Exception as e:

            jsonc.m_Logger.error( 'Can not open file "{}"\n{}', filenm if filenm else 'object', e );

        return {};
