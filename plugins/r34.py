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
    """Re-post a random image from https://rule34.usMake the bot say something"""

    if interaction.channel.is_nsfw():
        await interaction.response.send_message( '<:walter_what:1278078147870331011>', delete_after=10 )
    else:
        await interaction.response.send_message( "This command only works on NSFW Channels" );
        return;

    try:

        tags = tags.split( ' ' );

        url = get_r34_post( tags, page );

        if url:

            media: discord.Message = await interaction.channel.send(url);

            await media.add_reaction('❌');

            await asyncio.sleep( 30 );

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
