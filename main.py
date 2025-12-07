"""
The MIT License (MIT)

Copyright (c) 2025 Mikk155

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from src.Bot import Bot;

bot: Bot = Bot();

# Events
from src.events import on_error;
from src.events import on_guild_channel_pins_update;
from src.events import on_guild_emojis_update;
from src.events import on_guild_stickers_update;
from src.events import on_invite;
from src.events import on_member_join;
from src.events import on_member_remove;
from src.events import on_message;
from src.events import on_message_delete;
from src.events import on_message_edit;
from src.events import on_reaction;
from src.events import on_ready;
from src.events import on_think;
from src.events import on_typing;
from src.events import on_audit_log_entry_create;
from src.events import on_disconnect;

import src.libs.shutdown;
import src.libs.trusted;

import os;

bot.dirname = os.path.dirname( __file__ );

bot.run( token = open( os.path.join( bot.dirname, "token.txt" ), "r" ).readline(), reconnect = True );
