import datetime;
import pytz;

global g_Utils;
class g_Utils:

    '''
        Utility methods
    '''

    @staticmethod
    def time() -> datetime.datetime:
        '''
            Get the curret time for the bot zone
        '''
        return  datetime.datetime.now( pytz.timezone( "America/Argentina/Cordoba" ) );
