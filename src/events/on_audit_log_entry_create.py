'''
    Event called when audit log gets a new entry
'''

from __main__ import bot;
from src.Bot import Bot;
bot: Bot;

import discord;

@bot.event
async def on_audit_log_entry_create( entry: discord.audit_logs.AuditLogEntry ):

    try:

        ''''''

    except Exception as e:

        bot.exception( f"on_audit_log_entry_create: {e}" );

