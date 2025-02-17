import datetime
import pytz

def timezone() -> datetime.datetime:
    return  datetime.datetime.now( pytz.timezone( "America/Argentina/Cordoba" ) )
