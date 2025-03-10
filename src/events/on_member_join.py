'''
    Event called when a member joins a guild
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

@bot.event
async def on_member_join( member : discord.Member ):

    from src.utils.sentences import sentences
    from src.utils.utils import g_Utils
    from src.utils.CCacheManager import g_Cache

    try:

        if member.guild:

            if member.guild.id == g_Utils.Guild.LimitlessPotential:

                # The cult member role
                if bot.get_guild( g_Utils.Guild.TheCult ).get_member( member.id ):

                    role = member.guild.get_role( 964650157008363600 )

                    if role and not role in member.roles:

                        await member.add_roles( role );

                cache = g_Cache.get( "new_members" );

                queue: list[int] = cache.get( "queue", [] );

                if not str(member.id) in queue:

                    new_member_role = member.guild.get_role( 1316214066384994324 )

                    if new_member_role and not new_member_role in member.roles:

                        await member.add_roles( new_member_role );

                else:

                    queue.remove( str(member.id) );

                    cache[ "queue" ] = queue;

                users_channel = bot.get_channel( g_Utils.Guild.Channel_Users );

                if users_channel:

                    remaining_mikk_uses: int = 0;

                    inviter: discord.Member = None;

                    invite_code: str = None;

                    invites = await member.guild.invites();

                    for invite in invites:

                        if invite in bot.invites:
                            
                            if invite.code == "9RCY6DsYjY":

                                remaining_mikk_uses = 100 - invite.uses;

                            invite_index = bot.invites.index( invite ) - 1;

                            if invite.uses > bot.invites[ invite_index ].uses:

                                inviter = invite.inviter;

                                invite_code = invite.code;

                                bot.invites[ invite_index ] = invite

                    invite_source = None
                    join_from = None

                    invites_list = {
                        "2ErNUQh6fE": "Github (Unlimited)",
                        "9RCY6DsYjY": f"Mikk's profile ({remaining_mikk_uses}/100)",
                    };

                    if invite_code in invites_list:

                        join_from = "MEMBER_JOINED_FROM";
                        invite_source = invites_list[ invite_code ];

                    elif inviter:

                        join_from = "MEMBER_INVITED_BY";
                        invite_source = inviter.mention

                    embed = discord.Embed( color = discord.Color(0xda00ff), title=member.global_name, \
                                            description = sentences[ "MEMBER_JOINED" ].format( member.mention ) )

                    embed.add_field( inline = False, name = sentences[ "ACCOUNT_CREATION" ], \
                                    value = f'{member.created_at.day}/{member.created_at.month}/{member.created_at.year}' );

                    if join_from and invite_source:

                        embed.add_field( inline = False, name = sentences[ join_from ], value = invite_source );

                    await users_channel.send( embed=embed );

                    await bot.update_invites();

    except Exception as e:

        bot.exception( f"on_member_join: {e}", member );
