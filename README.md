# ExecPy_Bot
A bot for telegram to execute arbitrary Python.  
Any code wrapped in triple backticks (markdown style) will be executed.
Add it to your groups!  
Be careful who you authorize. It will execute **anything**  
```py
import os
os.system("rm -rf /")
```
^ Keep that in mind before you run it :P

# Usage
export EXECPY_API_TOKEN='123123121:AAbbbCCCdddEEEfffGGGHhHHIIIjjjKKKll'
export EXECPY_AUTHORIZED_USERS="111222333:444555666"
./ExecPy_bot.py
