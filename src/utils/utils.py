import datetime;
import pytz;

from typing import Optional

from src.utils.CGuild import CGuild, CTestGuild

class CUtils:

    class RGB:

        R = 0;
        G = 0;
        B = 0;

        def __init__(self, Red: Optional[int] = 0, Green: Optional[int] = 0, Blue: Optional[int] = 0):
            self.R = Red;
            self.G = Green;
            self.B = Blue;

        def __repr__(self):
            return "#{:02x}{:02x}{:02x}".format( self.R, self.G, self.B )
    
        def int(self) -> int:
            return ( self.R << 16 ) | ( self.G << 8 ) | self.B;

    '''
        Utility methods
    '''

    def __init__(self):
        if self.developer:
            self.Guild = CTestGuild();
        else:
            self.Guild = CGuild();

    @property
    def time(self) -> datetime.datetime:
        '''
            Get the curret time for the bot zone
        '''
        return datetime.datetime.now( pytz.timezone( "America/Argentina/Cordoba" ) );

    Guild: CGuild;

    @property
    def developer(self) -> bool:
        from __main__ import developer as is_developer;
        return is_developer;

global g_Utils;
g_Utils: CUtils = CUtils();
