# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
import os
import datetime   as dt
import globalFile as gn

helpStr = """
Greets the user.
Syntax:
    GREET [format]
Options:
    format -> Specify format to greet the user.
              1 - Format: "Hello *user*" (default)
              2 - Format: "Good*morning|afternoon|evening|night*, *user*
"""

def GREET(interpreter, args):
    "Greets the user."
    try:
        if (args in ('', '-1')) or args.isspace():
            greetStr = f"Hello,"
        
        elif args == '-2':
            time = int(dt.datetime.now().strftime("%H"))
            if time in range(12):
                greetStr = f"Good morning,"
            elif time in range(12, 16):
                greetStr = f"Good afternoon,"
            elif time in range(16,24):
                greetStr = f"Good evening,"
        
        # That's mode 3, or INVALID!
        else:
            greetStr = "??That's invalid syntax##,"
        
        print(str(greetStr) + f" {gn.BLUE if gn.ANSI else ''}{os.getlogin()}!{gn.RESET if gn.ANSI else ''}")
        return 0
    
    except Exception as e:
        return gn.unknownErr("greet", e)
