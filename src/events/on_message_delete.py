from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;
from src.const import TheCult, LimitlessPotential, Colors;

@bot.event
@bot.exception
async def on_message_delete( message: discord.Message ) -> None:
#
    if not message.guild:
        return;

    deleter: discord.Member = None;

    try:
    #
        async for entry in message.guild.audit_logs( limit=5, action=discord.AuditLogAction.message_delete ):
        #
            if entry.target.id == message.author.id \
            and entry.target.mes == message.channel.id \
            and ( discord.utils.utcnow() - entry.created_at ).total_seconds() < 2:
            #
                deleter = entry.user;
                break;
            #
        #
    #
    except Exception:
        pass;

    logChannel: discord.TextChannel = None;

    if message.guild.id == LimitlessPotential.id:
    #
        logChannel = bot.get_channel( LimitlessPotential.Channels.DiscordLogs );
    #
    elif message.guild.id == TheCult.id:
    #
        logChannel = bot.get_channel( TheCult.Channels.DiscordLogs );
    #

    if logChannel and logChannel is not message.channel:
    #
        authorMention: str = message.author.mention;

        if message.webhook_id is not None: # Is this a webhook?
        #
            WebHookAt: list[discord.Webhook] = [ w for w in await message.channel.webhooks() if w.id == message.webhook_id ];

            if len(WebHookAt) > 0:
            #
                authorMention = f'{authorMention} (Webhook ``{WebHookAt[0].name}``)';
            #
        #

        embed = discord.Embed(
            color = Colors.Red,
            title = "Message deleted",
            description = f"Message sent by {authorMention} deleted in {message.channel.jump_url}"
        );

        try: # Was this message a reply to another message?
        #
            if message.reference and message.reference.message_id:
            #
                replied: discord.Message = await message.channel.fetch_message( message.reference.message_id );
                if replied:
                    embed.description = f"{embed.description}\nThe message was a replied to {replied.jump_url}";
            #
        #
        except:
            pass;

        content: str = message.content;

        # Was it a text message? Could have been just a file
        if content:
        #
            # Split in parts if it's too long for embeding
            if len(content) > 1024:
            #
                part: int = 1;

                while len( content ) > 1024:
                #
                    content_part: str = content[ : 1024 ];
                    content = content[ 1024 : ];
                    embed.add_field( inline = False, name = f"Content split part {part}", value = content_part );
                    part += 1;
                # Send the remaining text
                if len(content) > 0:
                    embed.add_field( inline = False, name = f"Content split part {part}", value = content );
            #
            else:
            #
                embed.add_field( inline = False, name = f"Content", value = content );
            #
        #

        if message.attachments:
        #
            files_text = ""

            for i, a in enumerate( message.attachments, start = 1 ):
            #
                files_text += f"**{i}.** [{a.filename}]({a.url}) ({a.size/1024:.1f} KB)\n"
            #
            embed.add_field( name = "Attachments", value = files_text, inline = False );
        #

        if deleter: # Have this been reported to the audith log? If so then it was a moderator.
            embed.add_field( inline = False, name = "Message deleted by", value = f"<@{deleter.id}>" );

        # Did the message had some embeding? send them all
        if message.embeds and len( message.embeds ) > 0:
        #
            await logChannel.send( embeds = [ embed ] + message.embeds, allowed_mentions = False, silent = True );
        #
        else:
        #
            await logChannel.send( embed = embed, allowed_mentions = False, silent = True );
        #
    #
#
