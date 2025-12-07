from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

@bot.event
@bot.exception
async def on_audit_log_entry_create( entry: discord.audit_logs.AuditLogEntry ) -> None:
#
    pass;
#
