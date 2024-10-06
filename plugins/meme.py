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

from plugins.main import *

memes = {
    "argentina_lore": "https://cdn.discordapp.com/attachments/739984597114290196/1282781996258431006/FwGIbrAupXuBPAyW-1.mp4?ex=67023994&is=6700e814&hm=b5c8aac6999153d059b53d7dee42aed8d749d191bb6a825544e592798e0cafa5&",
    "fantasia_peruana": "https://www.youtube.com/watch?v=vdF7ANlKjAk",
    "trash_opinion": "https://cdn.discordapp.com/attachments/876568446039646289/1292180688543416363/aye_bruh_-_there_goes_your_opinion.mp4?ex=6702cc8b&is=67017b0b&hm=e7b7094efac8cbac2adc6461a8c203b7f6ebec21c14c9d2143a23c02b45d3bbe&",
};

meme_choic = {
    "Fantasia peruana": "fantasia_peruana",
    "Argentina lore": "argentina_lore",
    "Trash Opinion": "trash_opinion",
}

@bot.tree.command()
@app_commands.describe(
    meme='Meme',
)
@app_commands.choices( meme=gpUtils.to_command_choices( meme_choic ) )
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
