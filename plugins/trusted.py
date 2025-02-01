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

def on_initialization() -> dict:
    '''
    Called when the script is executed, this is the first hook ever called.

    The bot is not even initialized yet.

    This hook is required on all plugins and must return data.
    '''

    # Create data for g_PluginManager
    __data__: dict = {};
    __data__["name"] = "Trusted role features";
    __data__["description"] = "Allow members with Trusted role to use these features";

    # Return data for g_PluginManager
    return __data__;

@bot.tree.command()
@app_commands.guild_only()
@app_commands.describe(
    user='Member',
    days='days',
    hours='hours',
    minutes='minutes',
    seconds='seconds',
    reason='reason'
)
async def timeout(
    interaction: discord.Interaction,
    user: discord.Member,
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
    reason: typing.Optional[str] = ''
):
    """Timeout a member"""

    await interaction.response.defer( thinking=True );

    try:

        if user:

            if not interaction.guild.get_role( 1287938639342600356 ) in interaction.user.roles:
                await interaction.followup.send( "You can't use this command", ephemeral=True );
                return;

            if minutes + days + seconds + hours == 0:
                await interaction.followup.send( "You have to specify an amount of time.", ephemeral=True );
                return;

            time = '';

            if days > 0:
                time += f'{days}d';
            if hours > 0:
                time += f'{hours}h';
            if minutes > 0:
                time += f'{minutes}m';
            if seconds > 0:
                time += f'{seconds}s';

            reason_str = "" if reason == '' else f" Response: {reason}";
            delta = datetime.timedelta( minutes=minutes, days=days, seconds=seconds, hours=hours );
            await user.timeout( delta, reason=reason );
            await interaction.followup.send(
                    embed=discord.Embed(
                    title = f"{user.name} was timedout by {interaction.user.name}",
                    description = f"Time: {time}{reason_str}",
                    color = 16711680
                )
            );

    except Exception as e:

        await bot.exception_handle( e, interaction=interaction );
