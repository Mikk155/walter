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

from src.main import *

@bot.tree.command()
@app_commands.describe( timezone='Time zone' )
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
@app_commands.choices( timezone = g_Format.to_command_choices( COMMON_TIMEZONES() ) )
async def cfg_timezone( interaction: discord.Interaction, timezone: app_commands.Choice[str] ):
    """Set bot timezone for this server"""

    await interaction.response.defer( thinking=True );

    try:

        guild: int = interaction.guild_id;

        cache = g_Cache.get( "timezone.py" );

        cache[ str( interaction.guild_id ) ] = timezone.name;

        msg = g_Sentences.get( "bot.timezone", guild );

        await interaction.followup.send( g_Format.brackets( msg, [ timezone.name ] ) );

    except Exception as e:

        await bot.exception_handle( e, interaction=interaction );
