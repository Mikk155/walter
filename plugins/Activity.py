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
    __data__["name"] = "Activity";
    __data__["description"] = "Update the bot's Activity status";
    __hooks__: list[Hooks] = [ Hooks.on_think ];
    __data__["hooks"] = __hooks__;

    g_Sentences.push_back( "Activity" );

    # Return data for g_PluginManager
    return __data__;


global g_Activity;
class CActivity:

    def choices( self ) -> dict:
        '''
        Return a list of Activity events
        '''
        return {
            "unknown": "-1",
            "playing": "0",
            "streaming": "1",
            "listening": "2",
            "watching": "3",
            "custom": "4",
            "competing": "5",
    };

    name: str

    type: int

    state: int

    states: list

    intervals: int

    time: datetime.datetime

    def __init__( self ):

        self.name = '';
        self.type = 1;
        self.state = 0;
        self.states = []
        self.intervals = 5;
        self.time = bot.time();

        self.update(self.time);

    def get_state( self ) -> int:

        '''Get next state in the states list'''

        self.state += 1;

        if self.state > len( self.states ):

            self.state = 1;

        return self.states[ self.state - 1 ];

    def update( self, now: datetime.datetime ) -> None:

        '''Return whatever is time to update Activity'''

        cache = g_Cache.get();

        self.states = cache.get( 'states', [] );

        if len( self.states ) == 0:
            self.states.append( "None" );

        self.intervals = cache.get( 'interval', 5 );

        self.type = cache.get( 'activity', 1 );

        self.name = cache.get( 'name', '' );

        self.time = ( now + datetime.timedelta( seconds=self.intervals ) );

g_Activity: CActivity = CActivity();

async def on_think() -> int:

    try:

        now = bot.time()

        if g_Activity.time < now:

            g_Activity.update( now );

            pActivity = discord.Activity(
                type = g_Activity.type,
                name = g_Activity.name,
                state = g_Activity.get_state(),
            );

            if pActivity:

                await bot.change_presence( activity = pActivity );

    except Exception as e:

#        print( e )
        pass

    return HOOK_CONTINUE();

@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
@app_commands.describe(
    body_entries='Modify body entries, Separate with a semi-colon ``;``',
    interval_update='Set update intervals.',
    name='Activity name "Listening to {}"',
    activity='Activity type "Listening", "Streaming" etc.',
)
@app_commands.choices( activity=g_Format.to_command_choices( g_Activity.choices() ) )
async def cfg_activity(
    interaction: discord.Interaction,
    body_entries:str = None,
    interval_update:int = None,
    name:str = None,
    activity:app_commands.Choice[str] = None
):
    """Update the bot's Activity status"""

    await interaction.response.defer( thinking=True );

    try:

        if not IS_OWNER( interaction.user.id ):

            await interaction.followup.send(
                g_Sentences.get(
                    "only.owner",
                    interaction.guild_id,
                    [
                        g_Config.configuration[ "owner" ]
                    ]
                )
            );

            return;

        cache = g_Cache.get();

        if body_entries:

            entries = body_entries.split( ";" );

            cache[ 'states' ] = entries;

        if interval_update:

            cache[ 'interval' ] = int( interval_update );

        if name:

            cache[ 'name' ] = name;

        if activity:

            cache[ 'activity' ] = int( activity.value );

        await interaction.followup.send(
            g_Sentences.get(
                "Activity.updated",
                interaction.guild_id,
                [
                    json.dumps( dict( cache ), indent=4 )
                ]
            )
        );

    except Exception as e:

        await bot.exception_handle( e, interaction=interaction );
