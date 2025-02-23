import datetime;
import pytz;

from src.utils.CGuild import CGuild, CTestGuild

class CUtils:

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
