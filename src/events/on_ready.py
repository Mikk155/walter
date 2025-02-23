'''
    Event called when the bot is run for the first time.
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

async def on_ready():

    from src.utils.utils import g_Utils

    try:

        lp_guild = bot.get_guild( g_Utils.Guild.LimitlessPotential );

        if lp_guild:

            tc_role = lp_guild.get_role( 1311845801428910101 )

            for lp_member in lp_guild.members:

                try:

                    if lp_member:

                        tc_member = bot.get_guild( g_Utils.Guild.TheCult ).get_member( lp_member.id );

                        if tc_member:

                            if not tc_role in lp_member.roles:

                                await lp_member.add_roles( tc_role );

                        elif tc_role in lp_member.roles:

                            await lp_member.remove_roles( tc_role );

                except Exception as e:
                    print(e)

    except Exception as e:

        bot.exception( f"on_ready: {e}" );
