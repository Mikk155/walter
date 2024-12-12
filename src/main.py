"""
The MIT License (MIT)

Copyright (c) 2024 Mikk155

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

#=======================================================================================
# Default libraries
#=======================================================================================

import io
import os
import re
import sys
import pytz
import json
import difflib
import random
import asyncio
import aiohttp
import datetime
import typing

#=======================================================================================
# END
#=======================================================================================

#=======================================================================================
# Third party libraries
#=======================================================================================

import discord
from discord import app_commands
from discord.ext import commands, tasks

#=======================================================================================
# END
#=======================================================================================

#=======================================================================================
# This Source's libraries
#=======================================================================================

class snippet:
    '''
    Snippets

    When a function asks for this variable type it means that the alternative variable type is expected.

    But you can write the variable name so snippets.code-snippets recomends you specific values the function accepts.
    '''

from src.constdef import *

from src.utils.Path import g_Path
from src.utils.format import g_Format
from src.utils.CJsonCommentary import jsonc
from src.CConfigSystem import g_Config
from src.CSentences import g_Sentences

# These two needs to be initialized here.
g_Sentences.initialize();
g_Config.initialize();

from src.CLogger import CLogger, g_DelayedLog, g_Logger
from src.CPluginManager import g_PluginManager, Hooks
from src.CCacheManager import g_Cache
g_Cache.initialize();

from src.Bot import Bot

global bot
bot: discord.Client | Bot = Bot();


# app_commands
import src.commands.language
import src.commands.bot_cache
import src.commands.server_logger
import src.commands.timezone

#=======================================================================================
# END
#=======================================================================================
