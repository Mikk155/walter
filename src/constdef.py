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

def HOOK_CONTINUE() -> int:

    '''
    Returns the hook as "continue" status
    '''

    return 0;

def HOOK_HANDLED() -> int:

    '''
    Returns the hook as "handled" and next hooks from plugins in the list bellow this won't be called
    '''

    return 1;


def INVALID_INDEX() -> int:

    '''
    Returns an invalid index for integer comparations
    '''

    return -1;

def CHARACTER_LIMIT() -> int:
    '''
    Returns the Discord's character limits per discord.Message's content
    '''

    return 2000;


def DEVELOPER() -> bool:

    '''
    Returns whatever the bot has been run with the ``-dev`` argument
    '''

    from sys import argv;

    return ( '-dev' in argv );
