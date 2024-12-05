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

# -TODO allow server ops to decide what loggers to show

@bot.tree.command()
@app_commands.describe( channel='Channel' )
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
async def cfg_logger( interaction: discord.Interaction, channel: discord.TextChannel ):
    """Set logger channel for this bot"""

    await interaction.response.defer( thinking=True );

    try:

        guild: int = interaction.guild_id;

        cache = g_Cache.get();

        cache[ str( guild ) ] = channel.id;

        await interaction.followup.send( g_Sentences.get( "logger.channel.set", guild ) );

    except Exception as e:

        await bot.exception_handle( e, interaction=interaction );
