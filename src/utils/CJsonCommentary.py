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

from src.main import *

class jsonc:

    '''
    Json Commentary
    '''

    m_Logger = CLogger( "Json" );

    @staticmethod
    def __format__( object : list[str] | str ) -> dict | list:

        __js_split__ = '';

        if isinstance( object, str ):

            __js_split__ = object;
        
        else:

            for __line__ in object:

                __line__ = __line__.strip();

                if __line__ and __line__ != '' and not __line__.startswith( '//' ):

                    __js_split__ = f'{__js_split__}\n{__line__}';

        try:

            js = json.loads( __js_split__ );

            return js;

        except Exception as e:

            debug = jsonc.m_Logger.error( 'Failed to open jsonc object: {}'.format( e ) );

        return {};

    @staticmethod
    def load( object: str ) -> dict | list:

        '''
        Open a json file ignoring single-line commentary

        Returns empty dict if an Exception is thrown

        **object** Path to a json file or a string with json format
        '''

        if object.endswith( '.json' ):

            if os.path.exists( object ):

                with open( object, 'r' ) as __file__:
        
                    object = __file__.readlines();
        
            else:

                __e__ = jsonc.m_Logger.critical( "File plugins.json doesn't exists!" );
                return jsonc.__format__( ["{}"] );

        return jsonc.__format__(object);
