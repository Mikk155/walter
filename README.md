# discord-bot

```
pip install -r requirements.txt
```

This bot template has a hooking system, Create your modules in ``plugins\`` to do your stuff.

# hooking system

Import ``main``:
```python
from plugins.main import *
```

Initialise an array of Hooks:
```python
hooks = [
    Hooks.on_think
];
```

Register these hooks:
```python
Plugin( plugin_name='Activity', hook_list=hooks );
```
- Note: it is important for ``plugin_name`` to be the plugin's filename.

Available hooks:
```python
async def on_ready():
async def on_think():
async def on_member_join( member : discord.Member ):
async def on_member_remove( member : discord.Member ):
async def on_message( message : discord.Message ):
async def on_message_delete( message : discord.Message ):
async def on_message_edit( Args : HookValue.message_delete ):
async def on_reaction_add( Args : HookValue.reaction ):
async def on_reaction_remove( Args : HookValue.reaction ):
```

### Commands

Create an instance of Commands class
```python
command = Commands();
```

Explicitly set this command to be only useable on specific servers
```python
command.servers = [  int('your server ID'), 123456789 ];
```

Same as servers. this is for expecific roles
```python
command.allowed = [  int('your role ID'), 123456789 ];
```

Print information when a user uses the help command
```python
command.information = '''
Print's hello world message
'''
```

Register your function
```python
command.function = 'on_command'
```

Finally register the command
```python
RegisterCommand( plugin_name='cmd_helloworld', command_name='hello', command_class=command );
```

```python
async def on_command( message: discord.Message, arguments: dict ):
    await message.reply( "Hello world" );
```

``arguments`` will be a list of passed-on arguments separated by commas.

If a provided argument contains a ``=`` between two strings it will be splited and the first argument will be the key pair of ``arguments`` instead of a enumeration.

```
!command argument 1, arg=argument 2, argument 3
```
That would lead to a dict like this:
```json
{
    "1": "argument 1",
    "arg": "argument 2",
    "2": "argument 3"
}