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
    git='Fetch Github changes and pull commits',
)
async def update( interaction: discord.Interaction, git: bool = False ):
    """Update bot"""

    await interaction.response.send_message( '<:walter_what:1278078147870331011>', ephemeral=True, delete_after=0.1 )

    pull = False;

    try:

        if git:

            repo = Repo( gpGlobals.abs() );

            origin = repo.remotes.origin;

            origin.fetch();

            commits_behind = repo.iter_commits( 'HEAD..origin/main' );

            changes = sum( 1 for _ in commits_behind );

            if changes > 0:

                await interaction.channel.send( 'The local repository is out of date. Pulling changes... {}'.format( changes ) );

                origin.pull();
            
                pull = True;

            else:

                await interaction.channel.send( 'The upstream repository is up to date.' );

    except:
        pass

    if interaction.user.id != 744768007892500481 and not pull:

        await interaction.channel.send( '{} Only Mikk can restart this bot.'.format( interaction.user.mention ) );

        return;

    await interaction.channel.send( 'Restarting.. [gif](https://tenor.com/view/do-not-run-python-python-computer-python-coding-coding-funny-coding-meme-gif-10365831290651691441)' );

    bot_path = os.path.join( os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) ), 'bot.py' );

    await bot.close();

    # -TODO Pass on all the arguments
    os.execv( sys.executable, [ sys.executable, bot_path, '-dev' if gpGlobals.developer() else '' ] );
