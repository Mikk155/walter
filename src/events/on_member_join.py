from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

from random import randint;
from src.const import LimitlessPotential, TheCult, Colors;
from src.utils.RGB import RGB;

def random_enter_message( member: discord.Member, server: int ) -> str:

    if server == LimitlessPotential.id:
    #
        match randint( 0, 35 ):
        #
            case 0: return f"New test subject detected: <@{member.id}>. Biohazard clearance level pending.";
            case 1: return f"<@{member.id}> has joined the sector. Report to anomalous materials lab immediately.";
            case 2: return f"Transit system online. <@{member.id}> now arriving to Sector C";
            case 3: return f"Attention: <@{member.id}> has joined. Surveillance teams remain alert.";
            case 4: return f"Access granted for <@{member.id}>.";
            case 5: return f"<@{member.id}> has arrived. human resistance population rising.";
            case 6: return f"<@{member.id}> materialized via Xen portal.";
            case 7: return f"<@{member.id}> connected. HEV suit initialized.";
            case 8: return f"A new co-op partner has arrived: <@{member.id}>. Don't let them push all the buttons.";
            case 9: return f"Please <@{member.id}> proceed to the anomalous materials lab.";
            case 10: return f"<@{member.id}> is here! Somebody give them a crowbar.";
            case 11: return f"<@{member.id}> connected — let's hope they brought the pizza.";
            case 12: return f"<@{member.id}> has joined the server. Spawning more enemies...";
            case 13: return f"<@{member.id}> loaded in. Terrain is still generating...";
            case 14: return f"<@{member.id}> joined the session. Navmesh rebuilding...";
            case 15: return f"<@{member.id}> has connected. AI nodes updated.";
            case 16: return f"<@{member.id}> joined the server — entity limit increased by +1.";
            case 17: return f"Error: <@{member.id}> is used but not initialised";
            case 18: return f"Warning: object <@{member.id}> is declared but never used";
            case 19: return f"A new test subject has entered: <@{member.id}>.";
            case 20: return f"<@{member.id}> just slipped into the server. Everyone act natural.";
            case 21: return f"Look who just arrived! Welcome, <@{member.id}>!";
            case 22: return f"A wild <@{member.id}> has appeared!";
            case 22: return f"Brace yourselves... <@{member.id}> has entered the server.";
            case 24: return f"<@{member.id}> just teleported in.";
            case 25: return f"New challenger approaching: <@{member.id}>!";
            case 26: return f"<@{member.id}> has brought the pizza";
            case 27: return f"<@{member.id}> just spawned here.";
            case 28: return f"Welcome aboard, <@{member.id}>! We've been expecting you... maybe.";
            case 29: return f"Hey <@{member.id}>, make yourself at home!";
            case 30: return f"<@{member.id}> Welcome, Welcome to city 17.";
            case 31: return f"<@{member.id}> just arrived! Quick, pretend we're doing something productive.";
            case 32: return f"<@{member.id}> joined. The server's power level increased.";
            case 33: return f"Incoming transmission... <@{member.id}> is now connected.";
            case 34: return f"<@{member.id}> joined. everyone hide the bread slices!";
            case 35: return f"<@{member.id}> stepped into the realm.";
    #
    elif server == TheCult.id:
    #
        match randint( 0, 4 ):
        #
            case 0: return f"<@{member.id}> Just slid in... try not to stare too obviously";
            case 1: return f"“Careful-<@{member.id}> has arrived, and the temperature just went up a bit";
            case 2: return f"Look who wandered into the danger zone. Welcome <@{member.id}>";
            case 3: return f"Everyone act natural, <@{member.id}> is here. or don't, They might like it.";
            case 4: return f"Welcome <@{member.id}>. The server was behaving until now.";
        #
    #
    return f"<@{member.id}> joined the server.";
#

@bot.event
@bot.exception
async def on_member_join( member : discord.Member ) -> None:
#
    if not member or not member.guild:
        return;

    rules_id: int = None;
    channel_id: int = None;
    Color: Colors = None;
    inviteList: dict[str, int] = {};

    if member.guild.id == LimitlessPotential.id:
    #
        channel_id = LimitlessPotential.Channels.Users;
        rules_id = LimitlessPotential.Channels.Information;
        Color = Colors.LimitlessPotential;
        inviteList = LimitlessPotential.Invites;
    #
    elif member.guild.id == TheCult.id:
    #
        channel_id = TheCult.Channels.Users;
        rules_id = LimitlessPotential.Channels.Information;
        Color = Colors.TheCult;
        inviteList = TheCult.Invites;
    #

    if rules_id is not None:
    #
        rules_channel: discord.TextChannel = member.guild.get_channel( rules_id );

        if rules_channel:
        #
            welcum = f"Welcome to {member.guild.name}!\nBy staying here you agree to abide by our rules.\nYou can find them at {rules_channel.jump_url}";

            try:
                await member.send( welcum );
            except:
                pass;
        #
    #

    if channel_id is not None:
    #
        channel: discord.TextChannel = member.guild.get_channel( channel_id );

        embed = discord.Embed(
            color=Color,
            title=f"{member.name} joined the server.",
            description = random_enter_message( member, member.guild.id )
        );

        avatar: str | None = member.avatar.url if member.avatar else None;

        embed.set_author( name=member.name, icon_url=avatar, url=avatar );

        embed.add_field(
            inline = False,
            name = "Account creation",
            value = f'{member.created_at.day}/{member.created_at.month}/{member.created_at.year}'
        );

        GuildInvites: list[discord.Invite] = await member.guild.invites();

        for currentInvite in GuildInvites:
        #
            if currentInvite.uses > inviteList.get( currentInvite.code, 0 ):
            #
                inviteList[ currentInvite.code ] = currentInvite.uses;
        
                match currentInvite.code:
                #
                    case '2ErNUQh6fE': # *
                    #
                        embed.add_field( inline = False, name = "Joined by", value = "Static unlimited invite" );
                    #
                    case '9RCY6DsYjY': # 100
                    #
                        embed.add_field( inline = False, name = "Joined by", value = f"Game server {currentInvite.uses}/100" );
                    #
                    case 'ksY4XmBDfC': # 50
                    #
                        embed.add_field( inline = False, name = "Joined by", value = f"Mikk's Steam profile {currentInvite.uses}/50" );
                    #
                    case 'Wm8WqCSCUX': # 25
                    #
                        embed.add_field( inline = False, name = "Joined by", value = f"Mikk's Github profile {currentInvite.uses}/25" );
                    #
                    case 'HHMZj3MSWT': # 10
                    #
                        embed.add_field( inline = False, name = "Joined by", value = f"Mikk's Discord profile {currentInvite.uses}/10" );
                    #
                    case _:
                    #
                        inviter: discord.User | None = currentInvite.inviter;

                        if inviter:
                        #
                            embed.add_field( inline = False, name = "Invited by", value = f"<@{inviter.id}>" );
                            embed.set_footer( text=inviter.name, icon_url=inviter.avatar.url if inviter.avatar else None );
                        #
                        else:
                        #
                            embed.add_field( inline = False, name = "Invite used:", value = f"``{currentInvite.code}``" );
                        #
                    #
                #
            #
        #

        await channel.send(
            embed=embed,
            silent=True,
            allowed_mentions=False
        );
    #
#
