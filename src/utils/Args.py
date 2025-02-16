from sys import argv

def argument( name: str, default: str = None ) -> None | str:
    if name in argv and len(argv) > argv.index( name ):
        return argv[ argv.index( name ) + 1 ]
    return default
