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

import os
import json
from typing import Optional

class jsonc:

    '''
        Json Commentary
        Open a json file ignoring single-line commentary
    '''

    @staticmethod
    def load( file_path: str, *, exists_ok:Optional[bool]=None, cls=None, object_hook=None, parse_float=None,
        parse_int=None, parse_constant=None, object_pairs_hook=None, **kw) -> dict | list:
        """Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
        a JSON document) to a Python object.

        ``exists_ok`` if true and the file doesn't exist we'll create it and return a empty dict.

        ``object_hook`` is an optional function that will be called with the
        result of any object literal decode (a ``dict``). The return value of
        ``object_hook`` will be used instead of the ``dict``. This feature
        can be used to implement custom decoders (e.g. JSON-RPC class hinting).

        ``object_pairs_hook`` is an optional function that will be called with the
        result of any object literal decoded with an ordered list of pairs.  The
        return value of ``object_pairs_hook`` will be used instead of the ``dict``.
        This feature can be used to implement custom decoders.  If ``object_hook``
        is also defined, the ``object_pairs_hook`` takes priority.

        To use a custom ``JSONDecoder`` subclass, specify it with the ``cls``
        kwarg; otherwise ``JSONDecoder`` is used.
        """

        new_object = '';

        if os.path.exists( file_path ):

            object_lines = open( file = file_path, mode = 'r' ).readlines();

            for line in object_lines:

                line = line.strip();

                if line and line != '' and not line.startswith( '//' ):

                    new_object = f'{new_object}\n{line}';

        elif exists_ok:

            open( file_path, 'w' ).write( "{\n}" );

            return {};
    
        else:

            raise FileNotFoundError( f"Couldn't open file \"{file_path}\"" )

        return json.loads(new_object, cls=cls, object_hook=object_hook, parse_float=parse_float, parse_int=parse_int, parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kw);
