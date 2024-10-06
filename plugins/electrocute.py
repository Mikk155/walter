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
    member='Member',
)
async def electrocute( interaction: discord.Interaction, member: discord.Member ):
    """Electrocute a member and sent him to sleep"""

    try:

        if member.id == interaction.user.id:

            await interaction.response.send_message( '{} is going to mimir [media]({})'.format( interaction.user.mention, "https://cdn.discordapp.com/attachments/342709269017133064/1292115993040126083/SPOILER_youtube-jDgMkHB1pEI.mp4?ex=6702904b&is=67013ecb&hm=816913c613de3cd284f7765b3d13383b1251ee35bf62eee4d953c30c2cc004bb&" ) )

        else:

            await interaction.response.send_message( '{} Sent {} to mimir [media]({})'.format( interaction.user.mention, member.mention, "https://cdn.discordapp.com/attachments/342709269017133064/1292115993040126083/SPOILER_youtube-jDgMkHB1pEI.mp4?ex=6702904b&is=67013ecb&hm=816913c613de3cd284f7765b3d13383b1251ee35bf62eee4d953c30c2cc004bb&" ) )

    except Exception as e:

        await interaction.response.send_message( "Exception: {}".format( e ), ephemeral=True );
