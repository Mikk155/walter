from plugins.main import *

hooks = [
    Hooks.on_message,
    Hooks.on_ready
];

RegisterHooks( plugin_name='count_together', hook_list=hooks );

global count_together;
count_together = jsonc( '{}\\plugins\\count_together.json'.format( abspath ) );

@bot.tree.command()
async def cfg_counttogether( interaction: discord.Interaction ):
    """Configure this channel as a count-together channel"""

    try:

        if interaction.user.guild_permissions.administrator:
            count_together[ str(interaction.guild_id) ] = interaction.channel_id;
            open( '{}\\plugins\\count_together.json'.format( abspath ), 'w' ).write( json.dumps( count_together, indent = 0 ) );
            await interaction.response.send_message( "Configuration set, Now only counting on this channel." );
        else:
            await interaction.response.send_message( "Only administrators can use this command.", ephemeral=True );

    except Exception as e:
        await interaction.response.send_message( f"Exception: {e}" );

async def on_message( message: discord.Message ):

    if not message.author or message.author.id == bot.user.id or not message.guild or not str(message.guild.id) in count_together:
        return

    channel = bot.get_channel( int(count_together[ str(message.guild.id) ]) );

    if not channel or message.channel is not channel:
        return

    numero_actual = re.search( r'\b(\d+)\b', message.content )

    if numero_actual:

        numero_actual = int( numero_actual.group(1) )

    else:

        await message.delete()

        await message.channel.send( f'{message.author.mention} Only counting on this channel!', delete_after = 5 )

        return

    async for old_message in message.channel.history( limit=10, before=message.created_at ):

        if not old_message.content[0].isdigit():

            continue

        numero_anterior = re.search( r'\b(\d+)\b', old_message.content )

        if numero_anterior:

            numero_anterior = int(numero_anterior.group(1))

            break

    if numero_actual <= numero_anterior or numero_actual > numero_anterior + 1:

        if message:

            await message.delete()

        await message.channel.send( f'{message.author.mention}, do you know how to count? :face_with_raised_eyebrow:', delete_after = 5 )

async def on_ready():

    for guild, channel_id in count_together.items():

        channel = bot.get_channel( channel_id );

        if not channel:
            continue;

        numero_anterior = None;

        async for old_message in channel.history( limit=10 ):

            if old_message.author == bot.user:
                numero_anterior = None;
                break;

            if numero_anterior:
                continue

            if not old_message.content[0].isdigit():
                continue

            numero_anterior = re.search( r'\b(\d+)\b', old_message.content )

            if numero_anterior:

                numero_anterior = int(numero_anterior.group(1)) + 1

        if numero_anterior:

            await channel.send( f'{numero_anterior}')
