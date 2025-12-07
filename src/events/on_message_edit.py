from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;
import difflib;
from src.const import TheCult, LimitlessPotential, Colors;

@bot.event
@bot.exception
async def on_message_edit( before: discord.Message, after: discord.Message ) -> None:
#
    if not after.guild:
        return;

    logChannel: discord.TextChannel = None;

    if after.guild.id == LimitlessPotential.id:
    #
        logChannel = bot.get_channel( LimitlessPotential.Channels.DiscordLogs );
    #
    elif after.guild.id == TheCult.id:
    #
        logChannel = bot.get_channel( TheCult.Channels.DiscordLogs );
    #

    if logChannel:
    #
        embed = discord.Embed( color = Colors.Lime, title = "Message edited",
            description = f"Message sent by {after.author.mention} edited in {after.jump_url}"
        );

        old: str = before.content;
        new: str = after.content;

        matcher: difflib.SequenceMatcher[str] = difflib.SequenceMatcher( None, old, new );
        old_result: list[str] = [];
        new_result: list[str] = [];

        ShouldSend = False;

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        #
            if tag == 'equal':
            #
                old_result.append(old[i1:i2]);
                new_result.append(new[j1:j2]);
            #
            elif tag == 'replace':
            #
                old_result.append(f"<replace old>{old[i1:i2]}<>");
                new_result.append(f"<replace new>{new[j1:j2]}<>");
            #
            elif tag == 'delete':
            #
                old_result.append(f"<deleted>{old[i1:i2]}<>");
            #
            elif tag == 'insert':
            #
                new_result.append(f"<inserted>{new[j1:j2]}<>");
            #
        #

        old: str = ''.join( o for o in old_result );
        new: str = ''.join( o for o in new_result );

        if old != new:
        #
            def TuncateEmbeds( _newEmbed: discord.Embed, _Text: str, _Type: str ) -> discord.Embed:
            #
                _CurrentPart: int = 1;

                if len(_Text) > 1024:
                #
                    while len( _Text ) > 1024:
                    #
                        _Text_part: str = _Text[ : 1024 ];
                        _Text = _Text[ 1024 : ];
                        _newEmbed.add_field( inline = False, name = f"{_Type} part {_CurrentPart}", value = _Text_part );
                        _CurrentPart = _CurrentPart + 1;
                    #
                    if len( _Text ) > 0:
                        _newEmbed.add_field( inline = False, name = f"{_Type} part {_CurrentPart}", value = _Text );
                #
                else:
                    _newEmbed.add_field( inline = False, name = _Type, value = _Text );
            #

            TuncateEmbeds( embed, old, "Before" );
            TuncateEmbeds( embed, new, "New" );
            ShouldSend = True;
        #

        if before.attachments:
        #
            files_text: str = "";

            for i, a in enumerate( before.attachments, start = 1 ):
            #
                if not a in after.attachments:
                #
                    files_text += f"**{i}.** [{a.filename}]({a.url}) ({a.size/1024:.1f} KB)\n"
                #
            #

            if files_text != "":
            #
                embed.add_field( name = "Removed attachments", value = files_text, inline = False );
                ShouldSend = True;
            #
        #

        files_embeds: list[discord.Embed] = [];

        if before.embeds:
        #
            for e in before.embeds:
            #
                if not e in after.embeds:
                #
                    files_embeds.append( e );
                    ShouldSend = True;
                #
            #
        #

        if ShouldSend is True:
            await logChannel.send( embeds=[embed] + files_embeds, allowed_mentions=False, mention_author=False );
    #
#
