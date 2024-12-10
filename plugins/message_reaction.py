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
    __data__["name"] = "Message Reaction";
    __data__["description"] = "React to messages that contains certain words";
    __hooks__: list[Hooks] = [ Hooks.on_message ];
    __data__["hooks"] = __hooks__;

    # Return data for g_PluginManager
    return __data__;

@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions(manage_expressions=True)
@app_commands.describe(
    word='Word to match',
    emoji='Emoji name, leave empty for removing a word reaction, or use a space to set multiple emojis',
    file='Optional a whole json object containing the reactions cache.',
)
async def cfg_message_reaction(
    interaction: discord.Interaction,
    word: typing.Optional[str] = None,
    emoji: typing.Optional[str] = None,
    file: typing.Optional[discord.Attachment] = None
):
    """Configure message reactions, run w/o arguments to get a list"""

    await interaction.response.defer( thinking=True );

    try:

        cache = g_Cache.get();

        srv = cache.get( str( interaction.guild_id ), {} );

        cache[ str( interaction.guild_id ) ] = srv;

        if file:

            try:

                async with aiohttp.ClientSession() as session:

                    async with session.get( file.url ) as response:

                        if response.status == 200:

                            data = await response.read();

                            srv = json.loads( data );

                            cache[ str( interaction.guild_id ) ] = srv;

                            await interaction.followup.send( g_Sentences.get( 'updated.cache', interaction.guild_id ) );

                        else:

                            raise Exception( "Couldn't download the file." );

            except Exception as e:

                await interaction.followup.send( "Exception: {}".format( e ) );

        elif not word:

            emoji_list = json.dumps( srv, indent=0 );

            buffer = io.BytesIO( emoji_list.encode( 'utf-8' ) );

            buffer.seek(0);

            await interaction.followup.send( 'json', file=discord.File( buffer, "reactions.json" ) );

        elif not emoji:

            srv.pop( word, '' );

            cache[ str( interaction.guild_id ) ] = srv;

            await interaction.followup.send( g_Format.brackets( g_Sentences.get( 'item.removed', interaction.guild_id ), [ word ] ) );

        else:

            srv[ word ] = emoji;

            cache[ str( interaction.guild_id ) ] = srv;

            await interaction.followup.send( g_Format.brackets( g_Sentences.get( "item.set.to", interaction.guild_id ), [ word, emoji ] ) );

    except Exception as e:

        await bot.exception_handle( e, interaction=interaction );

async def on_message( message: discord.Message ):

    if not message.guild or message.author.id == bot.user.id:
        return HOOK_CONTINUE();

    cache = g_Cache.get();

    if not str( message.guild.id ) in cache:
        return HOOK_CONTINUE();

    message_reactions = cache.get( str( message.guild.id ), {} );

    for keyword, emotes in message_reactions.items():

        if keyword in message.content.lower():

            emote = emotes.split();

            for e in emote:

                try:

                    await message.add_reaction( e );

                except:

                    continue;

    return HOOK_CONTINUE();
