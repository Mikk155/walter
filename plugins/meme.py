from plugins.main import *

memes = {
    "argentina_lore": "https://cdn.discordapp.com/attachments/739984597114290196/1282781996258431006/FwGIbrAupXuBPAyW-1.mp4?ex=67023994&is=6700e814&hm=b5c8aac6999153d059b53d7dee42aed8d749d191bb6a825544e592798e0cafa5&",
    "fantasia_peruana": "https://www.youtube.com/watch?v=vdF7ANlKjAk",
};

MEMES_CHOICES = [
    app_commands.Choice(name='Fantasia peruana', value='fantasia_peruana' ),
    app_commands.Choice(name='Argentina lore', value='argentina_lore' ),
]

@bot.tree.command()
@app_commands.describe(
    meme='Meme',
)
@app_commands.choices( meme=MEMES_CHOICES )
async def meme( interaction: discord.Interaction, meme: app_commands.Choice[str], message: str = None ):
    """Reposts a meme"""

    try:
        media = memes[ meme.value ] if meme.value in memes else None;

        if media:

            text = '[media]({})'.format( media );

            if message:
                text = '{} {}'.format( message, text );

            await interaction.response.send_message( text );

        else:
            raise Exception( "No valid media selected" );

    except Exception as e:
        await interaction.response.send_message( "Exception: {}".format( e ), ephemeral=True );
