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

class g_DelayedLog:

    '''
    Delayed logs to discord channels
    '''

    delayed_logs: list[ list[ str | int | bool ] ] = [];

    def should_print() -> bool:
        '''Return whatever is time to print something to discord servers'''
        return bool( len( g_DelayedLog.delayed_logs ) > 0 );

    @staticmethod
    async def print_server(bot) -> None:

        '''
        Print all messages that has been delayed
        '''

        if not bot or bot is None:

            return;

        from src.constdef import INVALID_INDEX;
        from src.CConfigSystem import g_Config;

        while len( g_DelayedLog.delayed_logs ) > 0:

            await bot.wait_until_ready();

            try:
                message: str        = g_DelayedLog.delayed_logs[0][0];
                channel_id: int     = g_DelayedLog.delayed_logs[0][1];
                server_id: int      = g_DelayedLog.delayed_logs[0][2];
                is_log_server: bool = g_DelayedLog.delayed_logs[0][3];

                if is_log_server:

                    channel_id = g_Config.configuration[ "log_id" ];

                #elif server_id != INVALID_INDEX():

                    # -TODO Change channel_id with the cache's log id for the server with the current channel_id

                if channel_id != INVALID_INDEX():

                    channel = bot.get_channel( channel_id );
                
                    if channel:

                        await channel.send( content=message );

                g_DelayedLog.delayed_logs.pop(0);

            except:

                g_DelayedLog.delayed_logs.pop(0);

                pass

    from src.constdef import INVALID_INDEX;

    @staticmethod
    def delay(sentence: str, channel_id: int = INVALID_INDEX(), server_id: int = INVALID_INDEX(), is_log_server: bool = False) -> None:

        '''
        Delay a message if the bot is not ready
        '''

        g_DelayedLog.delayed_logs.append( [ sentence, channel_id, server_id, is_log_server ] );

class CLogger:

    '''
    Class Logger instance
    '''

    from src.main import snippet;

    __logger__: str = None;

    def get_name(self) -> str:

        '''
        Get the logger name
        '''

        return self.__logger__;

    def __init__( self, logger: str ) -> None:

        '''
            Initialise a logger
            **logger**: Name of the logger
        '''

        self.__logger__ = logger;

    def __print__(self, message:str, args:list=None, cmd:bool=True, dev:bool=False, channel:int=None, server:int=None, type:str=None, emoji:str=None) -> str:

        from src.CSentences import g_Sentences;

        sentence = g_Sentences.get( message, server );

        if type:

            type_sentence = g_Sentences.get( f'logger.{type}', server );

            sentence = f'[**{type_sentence}**] {sentence}';

        if self.get_name():

            sentence = f'[``{self.get_name()}``]{sentence}';

        else:

            sentence = f'[``{__name__}``]{sentence}';

        if args:

            for __arg__ in args:

                sentence = sentence.replace( "{}", str( __arg__ ), 1 );

        from src.CConfigSystem import g_Config;

        if type in g_Config.configuration.get( "loggers", [ "debug", "warning", "info", "trace" ] ):

            if cmd:

                print( sentence );

            if emoji:

                sentence = f'{emoji}{sentence}';

            if dev:

                g_DelayedLog.delay( sentence, is_log_server=True );

            if channel:

                g_DelayedLog.delay( sentence, channel_id=channel );

            if server:

                g_DelayedLog.delay( sentence, is_server_id=server );

        return sentence;

    def warn(self, message, args:list=None, cmd:bool=True, dev:bool=False, channel:int=None, server:int=None, type:str=None, emoji:str=None) -> str:
        return self.__print__( message, args, cmd, dev, channel, server, "warning", "⚠️" );

    def error(self, message, args:list=None, cmd:bool=True, dev:bool=False, channel:int=None, server:int=None, type:str=None, emoji:str=None) -> str:
        return self.__print__( message, args, cmd, dev, channel, server, "error", "‼️" );

    def debug(self, message, args:list=None, cmd:bool=True, dev:bool=False, channel:int=None, server:int=None, type:str=None, emoji:str=None) -> str:
        return self.__print__( message, args, cmd, dev, channel, server, "debug", "📝" );

    def info(self, message, args:list=None, cmd:bool=True, dev:bool=False, channel:int=None, server:int=None, type:str=None, emoji:str=None) -> str:
        return self.__print__( message, args, cmd, dev, channel, server, "info", "❕" );

    def critical(self, message, args:list=None, cmd:bool=True, dev:bool=False, channel:int=None, server:int=None, type:str=None, emoji:str=None) -> str:
        return self.__print__( message, args, cmd, dev, channel, server, "critical", "⛔" );

    def trace(self, message, args:list=None, cmd:bool=True, dev:bool=False, channel:int=None, server:int=None, type:str=None, emoji:str=None) -> str:
        return self.__print__( message, args, cmd, dev, channel, server, "trace", "➡" );

g_Logger = CLogger(None);
'''Global logger, the caller script will be passed on as a name'''