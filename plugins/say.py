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

@bot.tree.command()
@app_commands.describe(
    message='Say something',
#    reply='Message link to reply',
    user='User to stole identity (Administrator only)',
)
async def say( interaction: discord.Interaction, message: str, user: Optional[discord.Member] = None ):
    """Make the bot say something"""

    try:

        if user and interaction.user.guild_permissions.administrator:

            await interaction.response.send_message( '<:walter_what:1278078147870331011>', ephemeral=True, delete_after=0.1 )

            avatar = user.avatar.url;
            username = user.display_name;

            webhook = await interaction.channel.create_webhook( name='say_cmd' );

            await webhook.send( content=message, username=username, avatar_url=avatar );

            await webhook.delete()

        else:

            await interaction.response.send_message( message );

    except Exception as e:

        await interaction.response.send_message( "Exception: {}".format( e ), ephemeral=True );
