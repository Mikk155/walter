from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;
from src.const import TheCult, LimitlessPotential;

@bot.event
@bot.exception
async def on_ready() -> None:

    await bot.wait_until_ready();

    if bot.__Started__ is False: # This is the first time the bot is running. since on_ready is called multiple times
    #
        await bot.get_channel( LimitlessPotential.Channels.BotLogs ).send( f"Connected and logged as {bot.user.name}#{bot.user.discriminator}", silent=True );

        async def getInvites( target: TheCult | LimitlessPotential ) -> None:
        #
            targetGuild: discord.Guild = bot.get_guild( target.id );

            if targetGuild:
            #
                targetInvites: list[discord.Invite] = await targetGuild.invites();

                if targetInvites:
                #
                    for invite in targetInvites:
                    #
                        target.Invites[ invite.code ] = invite.uses;
                    #
                #
            #
        #

        await getInvites( TheCult );
        await getInvites( LimitlessPotential );

        bot.__Started__ = True;
    #
    else: # Otherwise this is called from a connection recovered
    #
        await bot.get_channel( LimitlessPotential.Channels.BotLogs ).send( f"Reconnected after connection lost", silent=True );
    #

    from src.events.on_think import on_think;
    if not on_think.is_running():
    #
        on_think.start();
    #
