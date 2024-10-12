from plugins.main import *

@bot.tree.command()
@app_commands.describe(
    word='Word to match',
    emoji='Emoji name, leave empty for removing a word reaction, or use a space to set multiple emojis',
    file='Optional a whole json object containing the reactions cache.',
)
async def cfg_message_reaction( interaction: discord.Interaction, word: str = None, emoji: str = None, file: Optional[discord.Attachment] = None ):
    """Configure message reactions, run w/o arguments to get a list"""

    try:

        if interaction.user.guild_permissions.manage_emojis:

            cache = gpGlobals.cache.get();

            srv: dict = cache.get( str( interaction.guild_id ), {} );

            if file:

                try:
                    async with aiohttp.ClientSession() as session:

                        async with session.get( file.url ) as response:

                            if response.status == 200:

                                data = await response.read();

                                srv = json.loads( data );

                                cache[ str( interaction.guild_id ) ] = srv;

                                await interaction.channel.send( AllocString( "updated.cache", [], interaction.guild_id ) );

                            else:

                                raise Exception( "Couldn't download the file." );

                except Exception as e:

                    await interaction.channel.send( "Exception: {}".format( e ) );

            elif not word:

                emoji_list = json.dumps( srv, indent=0 );

                buffer = io.BytesIO( emoji_list.encode( 'utf-8' ) );

                buffer.seek(0);

                await interaction.response.send_message( 'json', file=discord.File( buffer, "reactions.json" ) );

            elif not emoji:

                srv.pop( word, '' );

                cache[ str( interaction.guild_id ) ] = srv;

                await interaction.response.send_message( AllocString( "item.removed" , [ word ], interaction.guild_id ) );

            else:

                srv[ word ] = emoji;

                cache[ str( interaction.guild_id ) ] = srv;

                await interaction.response.send_message( AllocString( "item.set.to" , [ word, emoji ], interaction.guild_id ) );

        else:

            await interaction.response.send_message( AllocString( "no.permission", [ "manage_emojis" ], interaction.guild_id ) );

    except Exception as e:

        await bot.handle_exception( interaction, e );

async def on_message( message: discord.Message ):

    if not message.guild or message.author.id == bot.user.id:
        return Hook.Continue();

    cache = gpGlobals.cache.get();

    if not str( message.guild.id ) in cache:
        return Hook.Continue();

    message_reactions = cache.get( str( message.guild.id ), {} );

    for keyword, emotes in message_reactions.items():

        if keyword in message.content.lower():

            emote = emotes.split();

            for e in emote:

                try:

                    await message.add_reaction( e );

                except:

                    continue;

    return Hook.Continue();