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

from src.main import *

def on_initialization() -> dict:
    '''
    Called when the script is executed, this is the first hook ever called.

    The bot is not even initialized yet.

    This hook is required on all plugins and must return data.
    '''

    # Create data for g_PluginManager
    __data__: dict = {};
    __data__["name"] = "anti scam";
    __data__["description"] = "Checks for scammers posting repeated messages in a short period of time";
    __hooks__: list[Hooks] = [ Hooks.on_link, Hooks.on_think_minute ];
    __data__["hooks"] = __hooks__;

    g_Sentences.push_back( "anti_scam" );

    # Return data for g_PluginManager
    return __data__;

class CAntiScam:

    class cfg:

        default = [ False, 3, 2, False, 5 ];

        enabled = 0;

        spam = 1;

        spam_new = 2;

        kick = 3;

        timeout = 4;

    data: dict;

    def __init__( self ):

        self.data = {}

global g_antiscam;
g_antiscam: CAntiScam = CAntiScam();

@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
@app_commands.describe(
    enable='True enables False disables this feature',
    spam_times='How many times a member can spam the same link message?',
    spam_times_newers='How many times a Recently-joined member can spam the same link message?',
    kick_member='If true the member is kicked from the server, else timeout him',
    timeout_member='Time out member this many hours if not kick_member True',
)
async def cfg_antiscam(
    interaction: discord.Interaction,
    enable:bool = True,
    spam_times: typing.Optional[int] = None,
    spam_times_newers: typing.Optional[int] = None,
    kick_member: typing.Optional[bool] = None,
    timeout_member: typing.Optional[int] = None
):
    """Checks for scammers posting repeated messages in a short period of time"""

    await interaction.response.defer( thinking=True );

    try:

        cache = g_Cache.get();

        srv = cache.get( str( interaction.guild_id ), {} );

        config = srv[ "__config__" ] if "__config__" in srv else g_antiscam.cfg.default;

        config[g_antiscam.cfg.enabled] = enable;

        config[g_antiscam.cfg.spam] = spam_times if spam_times else g_antiscam.cfg.default[g_antiscam.cfg.spam];

        config[g_antiscam.cfg.spam_new] = spam_times_newers if spam_times_newers else g_antiscam.cfg.default[g_antiscam.cfg.spam_new];

        config[g_antiscam.cfg.kick] = kick_member if kick_member else g_antiscam.cfg.default[g_antiscam.cfg.kick];

        config[g_antiscam.cfg.timeout] = timeout_member if timeout_member else g_antiscam.cfg.default[g_antiscam.cfg.timeout];

        srv[ "__config__" ] = config;

        cache[ str( interaction.guild_id ) ] = srv;

        await interaction.followup.send( g_Sentences.get( 'enabled' if enable else 'disabled', interaction.guild_id ) );

    except Exception as e:

        await bot.exception_handle( e, interaction=interaction );

async def on_link( message: discord.Message, urls: list[str] ) -> int:

    if message.author and message.guild:

        guild_id = message.guild.id;

        member = message.author;

        cache = g_Cache.get();

        if not str( guild_id ) in cache:
            return;

        srv = cache[ str( guild_id ) ];

        __config__ = srv.get( "__config__", g_antiscam.cfg.default );

        if __config__[g_antiscam.cfg.enabled]:

            guild = g_antiscam.data.get( str( guild_id ), {} );

            author = guild.get( str( member.id ), {} );

            content = author.get( message.content, {} );

            timespam = content.get( "timespam", 0 ) + 1;

            content[ "timespam" ] = timespam;

            messages_id = content.get( str( message.channel.id ), [] );

            messages_id.append( message.id );

            content[  str( message.channel.id ) ] = messages_id;

            author[ message.content ] = content;

            guild[ str( member.id ) ] = author;

            recent = False;

            joined_at = member.joined_at

            if joined_at:

                time = datetime.datetime.now( datetime.timezone.utc );

                time_diff = time - joined_at;

                if time_diff.total_seconds() < 86400:

                    recent = True;

            if timespam > __config__[g_antiscam.cfg.spam] \
            or recent and timespam > __config__[g_antiscam.cfg.spam_new]:

                kick = __config__[g_antiscam.cfg.kick];

                reason = g_Sentences.get( "anti_scam.scammed", guild_id,
                    [
                        member.mention,
                        g_Sentences.get( "anti_scam.kicked", guild_id ) if kick else \
                        g_Sentences.get( "anti_scam.timeout", guild_id,
                            [
                                __config__[g_antiscam.cfg.timeout]
                            ]
                        )
                    ]
                );

                try:

                    if kick:

                        await member.kick( reason );

                    else:
        
                        timeout = datetime.timedelta( hours=__config__[g_antiscam.cfg.timeout] );

                        await member.timeout( timeout, reason=reason );

                except Exception as e:
                    pass;

                scam_data = guild.pop( str( member.id ), None );

                embed = discord.Embed( title = "Anti Scam", color = 16711680, description=reason );

                scam = scam_data[ message.content ];

                embed.add_field( inline = True,
                    name = g_Sentences.get( "message", guild_id ),
                    value = message.content
                );

                for k, v in scam.items():

                    if not k.isnumeric():

                        continue;

                    try:

                        cache_channel: discord.TextChannel = bot.get_channel( int(k) );

                        if cache_channel:

                            try:

                                embed.add_field( inline = True,
                                    name = g_Sentences.get( "channel", guild_id ),
                                    value = cache_channel.jump_url
                                );

                            except Exception as e:
                                pass;

                            for messages in v:

                                message_rm = await cache_channel.fetch_message( messages );

                                if message_rm:

                                    await message_rm.delete();

                    except Exception as e:
                        pass;

                # -TODO Debug to a proper channel
                if g_Config.configuration[ "log_channel" ] != INVALID_INDEX():
                    debg = bot.get_channel( g_Config.configuration[ "log_channel" ] );
                    if debg:
                        await debg.send( embed=embed );

            g_antiscam.data[ str( guild_id ) ] = guild;

    return HOOK_CONTINUE();

async def on_think_minute() -> int:

    copy_data = g_antiscam.data.copy();

    for guild_id, guild_data in copy_data.items():

        try:

            copy_guild_data = guild_data.copy();

            for user_id, user_data in copy_guild_data.items():

                try:

                    copy_user_data = user_data.copy();

                    for msg, msg_data in copy_user_data.items():

                        try:

                            copy_msg_data = msg_data.copy();

                            timespam = copy_msg_data.pop( "timespam", 0 ) - 1;

                            copy_msg_data[ "timespam" ] = timespam;

                            if timespam <= 0:

                                user_data.pop( msg, None );

                                continue;

                            user_data[ msg ] = copy_msg_data;

                        except Exception as e:
                            pass;

                    if len( user_data ) > 0:

                        guild_data[ user_id ] = user_data;

                    else:

                        guild_data.pop( user_id, None );

                except Exception as e:
                    pass;

            if len( guild_data ) > 0:

                g_antiscam.data[ guild_id ] = guild_data;

            else:

                g_antiscam.data.pop( guild_id, None );

        except Exception as e:
            pass;

    return HOOK_CONTINUE();
