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

            repo = Repo( abspath );

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

    os.execv( sys.executable, [ sys.executable, bot_path, '-dev' if gpGlobals.developer else '' ] );
