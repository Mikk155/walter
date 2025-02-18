import discord
from datetime import datetime

class Bot( discord.Client ):

    '''
    Discord BOT instance
    '''

    __on_start_called__: bool = False
    '''Temporal bool to know if this is the first time the bot is run and not a connection recovery.'''

    class ThinkDelta:
        from datetime import datetime
        Secod = datetime
        Minute = datetime
        Hour = datetime
        Day = datetime

    from src.utils.Logger import Logger
    m_Logger: Logger = Logger( "BOT" )

    developer: bool = False
    '''If argument ``-developer`` is ``1`` this will be true.'''

    from src.utils.CSentences import sentence as __sentences__
    sentences: __sentences__;

    def __init__( self, developer: bool = False ):

        self.developer = developer

        from src.utils.CSentences import sentence

        self.sentences = sentence()
        if self.sentences:
            self.m_Logger.trace( self.sentences.get( "OBJECT_INITIALISED", __name__ ) )

        super().__init__( intents = discord.Intents.all() )
        self.tree = discord.app_commands.CommandTree( self )

    async def setup_hook(self):

        if self.developer:
            from src.utils.constants import guild_testserver_id
            __MY_GUILD__ = discord.Object( id = guild_testserver_id() )
            self.tree.clear_commands( guild=__MY_GUILD__ )
            self.tree.copy_global_to( guild=__MY_GUILD__ )
            await self.tree.sync( guild=__MY_GUILD__ )
        else:
            await self.tree.sync()

    def exception( self, exception_obj: ( Exception | str ) ) -> discord.Embed:

        '''
            Build a ``discord.Embed`` class with the stack flow of the exception handled.
        '''

        from src.utils.Logger import LoggerColors, LoggerLevel
        embed = discord.Embed( color = LoggerColors.get( LoggerLevel.error, 0x196990 ), timestamp=self.timezone() )

        try:

            from sys import exc_info
            from os.path import abspath
            from traceback import extract_tb

            exc_type, exc_value, exc_traceback = exc_info()
            traceback_list = extract_tb(exc_traceback)

            for frame in traceback_list:
                filename = frame.filename.replace( abspath( "" ), '' )
                if "Python" in filename:
                    filename = filename[ filename.find( "Python" ) : ]
                embed.add_field( inline = False,
                    name = f"{frame.name} line {frame.lineno}",
                    value = f"```py\n{frame.line}``` `{filename}`"
                )

                if len( embed.fields ) > 24:
                    break

                embed.title = exc_type.__name__
                embed.description = str(exception_obj)
                embed.set_footer( text="This incident will be reported." )

        except Exception as e:

            embed = discord.Embed( color = 3447003, timestamp=self.timezone(), title=f'Exception raised during exception builder LOL:', description=e )

        from src.utils.Logger import logs
        logs.append(embed)

        return embed

    def response( self, description=None, error = False ) -> discord.Embed:
        if error:
            return discord.Embed( color=0xFF0000, title=f'⛔ Error', description=description )
        return discord.Embed( color=0x00FF00, title=f'✅ Response', description=description )
