from plugins.main import *

hooks = [
    Hooks.on_message
];

RegisterHooks( __file__, hook_list=hooks );

async def on_message( message: discord.Message ):

    if message.author.id == bot.user.id:
        return ReturnCode.Continue;

    mentioned_users = message.mentions

    for user in mentioned_users:

        mention = user.mention

        if mention.find( '!' ) != -1:
            mention = mention.replace( '!', '' );

        counts = json.load( open( '{}\\plugins\\ping_counter.json'.format( abspath ), 'r' ) );

        counts[ mention ] = [ counts[ mention ][ 0 ] + 1 if mention in counts else 1, user.name ];

        open( '{}\\plugins\\ping_counter.json'.format( abspath ), 'w' ).write( json.dumps( counts, indent=1));

@bot.tree.command()
@app_commands.describe(
    user='Member',
)
async def ping_count( interaction: discord.Interaction, user: discord.Member ):
    """Show how many times a user has been pinged"""

    try:

        user_mentioned = user.mention;

        if user_mentioned.find( '!' ) != -1:
            user_mentioned = user_mentioned.replace( '!', '' );

        counts = json.load( open( '{}\\plugins\\ping_counter.json'.format( abspath ), 'r' ) );

        times = 0 if not user_mentioned in counts else counts[ user_mentioned ][ 0 ]

        await interaction.response.send_message( "The user {} has been pinged {} times <:pingreee:911150900666572842>".format( counts[ user_mentioned ][ 1 ], times ))

    except Exception as e:

        await interaction.response.send_message( f"Exception {e}", ephemeral=True );
