'''
    Event called when audit log gets a new entry
'''

from __main__ import bot

import discord

@bot.event
async def on_audit_log_entry_create( entry: discord.audit_logs.AuditLogEntry ):
    pass
