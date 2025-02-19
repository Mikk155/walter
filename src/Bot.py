import io
import json
import aiohttp
import asyncio
import discord

from datetime import datetime
from typing import Optional

from src.utils.utils import g_Utils

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
    '''If ``-developer`` is ``1`` this will be true.'''

    from src.utils.CSentences import sentence as __sentences__
    sentences: __sentences__;

    def __init__( self, developer: Optional[bool] = False ):

        self.developer = developer

        from src.utils.CSentences import sentence

        self.sentences = sentence()
        if self.sentences:
            self.m_Logger.trace( self.sentences.get( "OBJECT_INITIALISED", "Discord Bot" ) ).print()

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

    def additional_info_data( self, obj ) -> None | dict[str, str]:

        if obj:

            data = {}

            if isinstance( obj, discord.Interaction ):
                if obj.channel:
                    data[ "channel" ] = obj.channel.jump_url
                if obj.user:
                    data[ "user" ] = obj.user.name
                if obj.guild:
                    data[ "guild" ] = obj.guild.name

            elif isinstance( obj, discord.Message ):
                if obj.channel:
                    data[ "channel" ] = obj.channel.jump_url
                if obj.author:
                    data[ "user" ] = obj.author.name
                data[ "message" ] = obj.jump_url
                if obj.guild:
                    data[ "guild" ] = obj.guild.name

            elif isinstance( obj, discord.Member ):
                data[ "user" ] = obj.name
                if obj.guild:
                    data[ "guild" ] = obj.guild.name

            if len(data) > 0:
                return data

        return None

    def exception( self, exception_obj: ( Exception | str ), additional_info = None ) -> discord.Embed:

        '''
            Build a ``discord.Embed`` class with the stack flow of the exception handled.
        '''

        try:

            additional_info = self.additional_info_data( additional_info );

        except Exception as e:

            self.m_Logger.error( "Failed to generate additional data dictionary: {}", e )

            additional_info = None

        from src.utils.Logger import LoggerColors, LoggerLevel
        embed = discord.Embed( color = LoggerColors.get( LoggerLevel.error, 0x196990 ), timestamp=g_Utils.time() )

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

                if len( embed.fields ) > ( 23 if additional_info else 24 ): # Save one slot for data if provided
                    break

                embed.title = exc_type.__name__

                embed.description = str(exception_obj)

                embed.set_footer( text="This incident will be reported." )

            if additional_info:

                embed.add_field( inline = False, name = f"Additional data", value = json.dumps( additional_info, indent=0 ) )

        except Exception as e:

            embed = discord.Embed( color = 3447003, timestamp=g_Utils.time(), title=f'Exception raised during exception builder LOL:', description=e )

        from src.utils.Logger import logs
        logs.append(embed)

        return embed

    def json_to_file( self, json_object: dict ) -> discord.File:

        json_serialized = json.dumps( json_object, indent=2 )

        buffer = io.BytesIO( json_serialized.encode( 'utf-8' ) )

        buffer.seek(0)

        return discord.File( buffer, "json.json" )

    async def file_to_json( self, json_file: discord.Attachment ) -> tuple[ dict, discord.Embed ]:

        data = None
        embed = None

        if not json_file.filename.endswith( '.json' ):

            embed = self.m_Logger.error( self.sentences.get( "ONLY_FORMAT_SUPPORT", "json" ) )

        else:

            async with aiohttp.ClientSession() as session:

                async with session.get( json_file.url ) as response:

                    if response.status == 200:

                        data_bytes = await response.read()

                        try:

                            data = json.loads( data_bytes )

                        except Exception as e:

                            embed = self.m_Logger.error( self.sentences.get( "INVALID_JSON_OBJECT", e ) )

                            return ( data, embed )

                        embed = self.m_Logger.error( self.sentences.get( "UPDATED_FILE" ) )

                    else:

                        embed = self.m_Logger.error( self.sentences.get( "FAIL_DOWNLOAD_FILE" ) )

        return ( data, embed )

    async def webhook( self, channel: discord.TextChannel ) -> discord.Webhook:
        
        webhooks: list[discord.Webhook] = await channel.webhooks()

        for webhook in webhooks:

            if webhook and webhook.name == "walter":

                return webhook

        return await channel.create_webhook( name="walter" );

    async def user_reacted( self, emoji: str, user: discord.Member | discord.User, message: discord.Message ) -> bool:

        if message and user:

            for reaction in message.reactions:

                if str(reaction.emoji) == emoji:

                    async for user_in_reaction in reaction.users():

                        if user == user_in_reaction:

                            return True;

        return False;
