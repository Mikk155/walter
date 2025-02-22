import datetime;
import random;
from src.utils.CCacheManager import g_Cache;
from src.utils.utils import g_Utils;

class CActivity:

    def choices( self ) -> dict:
        '''
        Return a list of Activity events
        '''
        return {
            "unknown": "-1",
            "playing": "0",
            "streaming": "1",
            "listening": "2",
            "watching": "3",
            "custom": "4",
            "competing": "5",
    };

    name: str;

    type: int;

    state: int;

    states: list;

    intervals: int;

    time: datetime.datetime

    def __init__( self ):

        self.name = '';
        self.type = 1;
        self.state = 0;
        self.states = []
        self.intervals = 5;
        self.time = g_Utils.time;

        self.update(self.time);

        random.shuffle( self.states );

    def get_state( self ) -> int:

        '''Get next state in the states list'''

        self.state += 1;

        if self.state > len( self.states ):

            self.state = 1;

            random.shuffle( self.states );

        return self.states[ self.state - 1 ];

    def update( self, now: datetime.datetime ) -> None:

        '''Return whatever is time to update Activity'''

        cache = g_Cache.get( "Activity" );

        self.states = cache.get( 'states', [] );

        if len( self.states ) == 0:
            self.states.append( "None" );

        self.intervals = cache.get( 'interval', 5 );

        self.type = cache.get( 'activity', 1 );

        self.name = cache.get( 'name', '' );

        self.time = ( now + datetime.timedelta( seconds=self.intervals ) );

global g_Activity;
g_Activity: CActivity = CActivity();
