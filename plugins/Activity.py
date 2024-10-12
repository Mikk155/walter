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

global Activity;

class Activity:

    __time__ = 0;
    __state__ = 1;

    @staticmethod
    def GetState() -> int:
        '''Get the next state in the states list'''

        Activity.__state__ += 1;

        cache = gpGlobals.cache.get();

        states = cache.get( 'states', [] );

        if Activity.__state__ > len( states ):
            Activity.__state__ = 1;

        return states[ Activity.__state__ - 1 ];

    @staticmethod
    def ShouldUpdate() -> int:
        '''Return whatever is time to update Activity'''

        cache = cache = gpGlobals.cache.get();

        Think, Activity.__time__ = gpGlobals.should_think( Activity.__time__, cache.get( 'interval', 5 ) );

        return Think;

    choices = {
        "unknown": "-1",
        "playing": "0",
        "streaming": "1",
        "listening": "2",
        "watching": "3",
        "custom": "4",
        "competing": "5",
    };

async def on_think():

    # Catch and ignore errors completelly
    try:

        if Activity.ShouldUpdate():

            cache = cache = gpGlobals.cache.get();

            pActivity = discord.Activity(
                type = cache.get( 'activity', 1 ),
                name = cache.get( 'name', 'Wankers' ),
                state = Activity.GetState(),
            );

            if pActivity:

                await bot.change_presence( activity = pActivity );

    except:

        return Hook.Continue();

    return Hook.Continue();

@bot.tree.command( guild=bot.get_guild( gpGlobals.LimitlessPotential.server_id ) )
@app_commands.choices( activity=gpUtils.to_command_choices( Activity.choices ) )
@app_commands.describe(
    body_entries='Modify body entries, json-object-list ``[ "message1", "message2", "etc" ]``',
    get_body_entries='Get body entries list.',
    interval_update='Set update intervals.',
    name='Activity name "Listening to {}"',
    activity='Activity type "Listening", "Streaming" etc.',
)
async def cfg_activity(
    interaction: discord.Interaction,
    body_entries:str = None,
    get_body_entries:bool = False,
    interval_update:int = None,
    name:str = None,
    activity:app_commands.Choice[str] = None
):
    """Update bot's activity, Use only one argument at once!"""

    try:

        if interaction.user.id != gpGlobals.LimitlessPotential.mikk_id:
            await interaction.response.send_message( AllocString( "only.owner", [], interaction.guild_id ) );

        else:

            cache = gpGlobals.cache.get();

            if body_entries:
                cache[ 'states' ] = json.loads( body_entries );
                await interaction.response.send_message( AllocString( "activity.updated", [ "states", cache[ 'states' ] ], interaction.guild_id ) );

            elif get_body_entries:
                await interaction.response.send_message( "```json\n{}```".format( json.dumps( cache.get( 'states', [] ) ) ) );
    
            elif interval_update:
                cache[ 'interval' ] = int(interval_update);
                await interaction.response.send_message( AllocString( "activity.updated", [ "interval", interval_update ], interaction.guild_id ) );

            elif name:
                cache[ 'name' ] = name;
                await interaction.response.send_message( AllocString( "activity.updated", [ "name", name ], interaction.guild_id ) );

            elif activity:
                cache[ 'activity' ] = int( activity.value );
                await interaction.response.send_message( AllocString( "activity.updated", [ "type", activity.name ], interaction.guild_id ) );

    except Exception as e:

        await bot.handle_exception( interaction, e );