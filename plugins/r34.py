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

def get_r34_post( tags : list, page ):

    for i, t in enumerate( tags ):
        tags[i] = t.strip( ' ' );

    tag_string = '+'.join(tags)
    tag_string = f'{tag_string}&page={page}'

    url = f'https://rule34.us/index.php?r=posts/index&q={tag_string}'

    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup( response.text, 'html.parser' )

    posts = soup.find_all('div', style='border-radius: 3px; margin: 0px 10px 15px 10px; overflow: hidden; height: 200px; ')

    if not posts:
        return None

    random_post = random.choice( posts )

    image_page_url = random_post.find( 'a' )[ 'href' ]

    image_page_response = requests.get( image_page_url )

    if image_page_response.status_code != 200:
        return None

    image_page_soup = BeautifulSoup(image_page_response.text, 'html.parser')

    if image_page_soup is None:
        return None

    content_push = image_page_soup.find( 'div', class_='content_push' )

    image_url = content_push.find( 'img' )[ 'src' ]

    if not image_url or image_url == 'v1/icons/heart-fill.svg': # Try video

        image_url = content_push.find( 'source', type="video/webm" )[ 'src' ]

    return image_url

@bot.tree.command()
@app_commands.describe(
    tags='Tags (separated by spaces)',
    page='Page number',
)
async def r34( interaction: discord.Interaction, tags: str = None, page: int = 0 ):
    """Re-post a random image from https://rule34.us"""

    if interaction.channel.is_nsfw():
        await interaction.response.send_message( '<:walter_what:1278078147870331011>', delete_after=0.1, ephemeral=True )
    else:
        await interaction.response.send_message( "This command only works on NSFW Channels" );
        return;

    try:

        tags = tags.split( ' ' );

        url = get_r34_post( tags, page );

        if url:

            media: discord.Message = await interaction.channel.send(url);

            await media.add_reaction('❌');

            await asyncio.sleep( 10 );

            media = await media.channel.fetch_message( media.id );

            for reaction in media.reactions:

                if str(reaction.emoji) == '❌':

                    users = await reaction.users().flatten();

                    if len(users) > 1:

                        await media.delete();

                        return

                    else:

                        await media.clear_reactions();
    except:
        pass
