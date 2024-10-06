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

# -TODO on_daily
async def on_ready():

    if gpGlobals.developer(): # When testing i'd probably call this multiple times on a day
        return Hook.Continue();

    birthdays = gpUtils.jsonc( '{}birthdays.json'.format( gpGlobals.absp() ) );

    date = datetime.now()

    for user, birthday in birthdays.items():

        if birthday[0] == date.month and birthday[1] == date.day:

            try: # Prevent a deleted-channel from breaking the chain loop

                await bot.get_channel( birthday[2] ).send( "Everyone wish a Happy Birthday to {}".format( user ) );

            except Exception as e:

                continue;

    return Hook.Continue();

month_choices = {
    "January": "1",
    "February": "2",
    "March": "3",
    "April": "4",
    "May": "5",
    "June": "6",
    "July": "7",
    "August": "8",
    "September": "9",
    "October": "10",
    "November": "11",
    "December": "12",
};

@bot.tree.command()
@app_commands.describe(
    month='month',
    day='day',
    user='Member to set (Administrators only)',
)
@app_commands.choices( month=gpUtils.to_command_choices( month_choices ) )
async def birthday( interaction: discord.Interaction, month: app_commands.Choice[str], day: int, user: Optional[discord.Member] = None ):
    """Set your birthday"""

    try:

        if user is None:

            user = interaction.user;

        else:

            if user != interaction.user and not interaction.user.guild_permissions.administrator:

                await interaction.response.send_message( "Only administrators can set other's birthday", ephemeral=True );

                return;

        mention = gpUtils.mention( user );

        birthdays = gpUtils.jsonc( '{}birthdays.json'.format( gpGlobals.absp() ) );

        birthdays[ mention ] = [ int( month.value ), day, interaction.channel_id ];

        open( '{}birthdays.json'.format( gpGlobals.absp() ), 'w' ).write( json.dumps( birthdays, indent = 0, separators=( ',', ':' ) ) );

        await interaction.response.send_message( "The user {} birthday has been set {} {} in this channel".format( mention, month.name, day ) )

    except Exception as e:

        await interaction.response.send_message( f"Exception {e}", ephemeral=True );
