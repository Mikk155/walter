from plugins.main import *

global gpEmojis;
gpEmojis = gpUtils.jsonc( "{}message_reaction.json".format( gpGlobals.absp() ) );

@bot.tree.command()
@app_commands.describe(
    word='Word to match',
    emoji='Emoji name, leave empty for removing a word reaction, or use a space to set multiple emojis',
)
async def message_reaction( interaction: discord.Interaction, word: str = None, emoji: str = None ):
    """Configure message reactions, run w/o arguments to get a list"""

    try:

        if interaction.user.guild_permissions.manage_emojis:

            srv: dict = gpEmojis.get( str( interaction.guild_id ), {} );

            if not word:

                await interaction.response.send_message( '```json\n{}```'.format( json.dumps( srv, indent=0 ) ) );

            elif not emoji:

                srv.pop( word, '' );

                gpEmojis[ str( interaction.guild_id ) ] = srv;

                open( '{}message_reaction.json'.format( gpGlobals.absp() ), 'w' ).write( json.dumps( gpEmojis, indent=0 ) );

                await interaction.response.send_message( 'Removed {}'.format( word ) );

            else:

                srv[ word ] = emoji;

                gpEmojis[ str( interaction.guild_id ) ] = srv;

                open( '{}message_reaction.json'.format( gpGlobals.absp() ), 'w' ).write( json.dumps( gpEmojis, indent=0 ) );

                await interaction.response.send_message( 'Updated word ``{}`` to {}'.format( word, emoji ) );
        else:

            await interaction.response.send_message( 'You need "Manage emoji" permission to use this command.' );

    except Exception as e:

        await interaction.response.send_message( 'Exception: {}'.format( e ) );

async def on_message( message: discord.Message ):

    if not message.guild or not str( message.guild.id ) in gpEmojis or message.author.id == bot.user.id:
        return Hook.Continue();

    message_reactions = gpEmojis[ str( message.guild.id ) ];

    for keyword, emotes in message_reactions.items():

        if keyword in message.content.lower():

            emote = emotes.split();

            for e in emote:

                try:

                    await message.add_reaction( e );

                except:

                    continue;

    return Hook.Continue();