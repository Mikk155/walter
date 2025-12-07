from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

from random import randint;
from src.const import LimitlessPotential, TheCult, Colors;

def random_leave_message( member: discord.Member, server: int ) -> str:

    if server == LimitlessPotential.id:
    #
        match randint( 0, 28 ):
        #
            case 0: return f"<@{member.id}> has left the facility. Security clearance revoked.";
            case 1: return f"<@{member.id}> packed their bags and logged off.";
            case 2: return f"<@{member.id}> escaped the server. Freedom!";
            case 3: return f"<@{member.id}> has vanished. Recommend searching nearby vents.";
            case 4: return f"<@{member.id}> has been relocated to an unknown Xen coordinate.";
            case 5: return f"Attention: <@{member.id}> has abandoned their post.";
            case 6: return f"<@{member.id}> was lost in the way to the test chamber.";
            case 7: return f"<@{member.id}> has gone missing. Security teams instructed not to question it.";
            case 8: return f"<@{member.id}> disconnected. All Xen portals recalibrated.";
            case 9: return f"<@{member.id}> stepped into a portal and failed to return.";
            case 10: return f"User <@{member.id}> no longer present. Possibly conscripted by the Combine.";
            case 11: return f"<@{member.id}> escaped Black Mesa before everything went to hell... lucky bastard.";
            case 12: return f"<@{member.id}> exited the environment. Sector swept clean.";
            case 13: return f"<@{member.id}> disconnected. Rumors suggest G-Man involvement.";
            case 14: return f"<@{member.id}> escaped the facility before the resonance cascade.";
            case 15: return f"<@{member.id}> vanished. Suspected cause: headcrabs.";
            case 16: return f"<@{member.id}> rage-quit after being no-clipped into a wall.";
            case 17: return f"<@{member.id}> has left the world. Destructing object";
            case 18: return f"<@{member.id}> exited the game — last seen noclipping into the void.";
            case 19: return f"<@{member.id}> has left. Their weaponbox dropped to the floor.";
            case 20: return f"<@{member.id}> Left the server, Map restarting in 10 seconds.";
            case 21: return f"<@{member.id}> vanished without a trace.";
            case 22: return f"<@{member.id}> left the server. We'll miss you... probably.";
            case 22: return f"And just like that... <@{member.id}> is gone.";
            case 24: return f"<@{member.id}> has disconnected from our reality.";
            case 25: return f"<@{member.id}> took the last slice of pizza and left.";
            case 26: return f"Poof! <@{member.id}> disappeared.";
            case 27: return f"Goodbye <@{member.id}>, we hardly knew you.";
            case 28: return f"<@{member.id}> has left. We hope to see them again someday.";
        #
    #
    elif server == TheCult.id:
    #
        match randint( 0, 1 ):
        #
            case 0: return f"<@{member.id}> has left. guess we were too spicy. Or not spicy enough.";
            case 1: return f"<@{member.id}> has left. The thirst levels decreased by 0.2%";
    #
    return f"<@{member.id}> left the server.";
#

@bot.event
@bot.exception
async def on_member_remove( member : discord.Member ) -> None:
#
    if not member or not member.guild:
        return;

    channel_id: int = None;
    Color: Colors = None;

    if member.guild.id == LimitlessPotential.id:
    #
        channel_id = LimitlessPotential.Channels.Users;
        Color = Colors.LimitlessPotential;
    #
    elif member.guild.id == TheCult.id:
    #
        channel_id = TheCult.Channels.Users;
        Color = Colors.TheCult;
    #

    if channel_id is not None:
    #
        channel: discord.TextChannel = member.guild.get_channel( channel_id );

        embed = discord.Embed(
            color=Color,
            title=f"{member.name} left the server.",
            description = random_leave_message( member, member.guild.id )
        );

        avatar: str | None = member.avatar.url if member.avatar else None;

        embed.set_author( name=member.name, icon_url=avatar, url=avatar );

        if member.joined_at:
        #
            embed.add_field(
                inline = False,
                name = "Member since",
                value = f'{member.joined_at.day}/{member.joined_at.month}/{member.joined_at.year}'
            );
        #

        await channel.send(
            embed=embed,
            silent=True,
            allowed_mentions=False
        );
    #
#
