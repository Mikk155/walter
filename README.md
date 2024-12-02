# discord-bot

Template discord bot that supports a "Plugin" implementation with a hooking system

```
pip install -r requirements.txt
```

- When adding third-party library make sure to include them in [main](plugins/main.py) so it's accesible by all plugins

## Plugin system

Create your python script in within ``./plugins/`` folder

Import ``main``:
```python
from src.main import *
```

Register your plugin in [plugins.json](plugins.json) following the instructions provided by the json [schema](schema.json)

- Create a ``tokens.txt`` file in the main folder and put in it your Discord Application BOT Token
    - Alternativelly you can add a second line with the token for running the bot with the ``-dev`` argument

### Pull requests are welcome and encouraged.
