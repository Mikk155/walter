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

async def on_daily():

    if gpGlobals.developer():
        return Hook.Continue();

    birthdays = gpUtils.jsonc( '{}birthdays.json'.format( gpGlobals.absp() ) );

    date = datetime.now()

    if str( date.month ) in birthdays:

        month = birthdays[ str( date.month ) ];

        if str( date.day ) in month:

            day = month[ str( date.day ) ];

            for channel_id, userdata in day.items():

                try: # Prevent a deleted-channel from breaking the chain loop

                    channel = bot.get_channel( int( channel_id ) );

                    for user_name, user_mention in userdata.items():

                        await channel.send( "Everyone wish a Happy Birthday to {}! <:kaleun:1212181960890253372> :tada:".format( user_mention ) );

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

        elif user.id != interaction.user.id and not interaction.user.guild_permissions.administrator:

            await interaction.response.send_message( "Only administrators can set someone else's birthday", ephemeral=True );

            return;

        birthday_list = gpUtils.jsonc( '{}birthdays.json'.format( gpGlobals.absp() ) );

        dmonth = birthday_list.get( month.value, {} )
        dday = dmonth.get( str( day ), {} )
        dchannel = dday.get( str( interaction.channel_id ), {} )
        dchannel[ user.global_name ] = user.mention;
        dday[ str( interaction.channel_id ) ] = dchannel;
        dmonth[ str( day ) ] = dday;
        birthday_list[ month.value ] = dmonth;

        open( '{}birthdays.json'.format( gpGlobals.absp() ), 'w' ).write( json.dumps( birthday_list, indent = 3, separators=( ',', ':' ) ) );

        await interaction.response.send_message( "The user {} birthday has been set {} {} in this channel".format( user.global_name, month.name, day ) );

    except Exception as e:

        await interaction.response.send_message( f"Exception {e}", ephemeral=True );
