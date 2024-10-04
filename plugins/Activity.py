from plugins.main import *

hooks = [
    Hooks.on_think
];

RegisterHooks( __file__, hook_list=hooks );

global Activity;
Activity = jsonc( '{}\\plugins\\Activity.json'.format( abspath ) );

global Activity_Time;
Activity_Time = 0;

global LastState;
LastState = 1;

async def on_think():

    global Activity_Time;

    if Activity_Time < gpGlobals.time:

        global Activity;
        global LastState;

        if LastState > len( Activity[ "State" ] ):
            LastState = 1;

        try:
            pActivity = discord.Activity(
                type = discord.ActivityType.listening,
                name = Activity[ "Activity" ],
                state = Activity[ "State" ][ LastState - 1 ],
            );

            await bot.change_presence( activity = pActivity );

        except:
            pass;

        LastState += 1;

        Activity_Time = gpGlobals.time + Activity[ "IntervalUpdate" ];
