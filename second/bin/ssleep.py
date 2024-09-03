# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
import time
import globalFile as gn
import intCommons as comm

helpStr = """
Waits a certain amount of time before continuing.
Syntax:
    SLEEP time
Argument:
    time -> Time to wait in seconds
"""

def SLEEP(interpreter, args, calledFrom="sleep"):
    "Waits a certain amount of time before continuing."
    try:
        args, opts = comm.parse(args)
        wait = 0
        if len(args) > 1:
            return gn.error(calledFrom, "Incorrect format")
        if len(opts) > 1:
            return gn.error(calledFrom, f"Too many options: {str(opts)[1:-1]}")
        if args:
            # Check if the argument is a number, floating point numbers are allowed
            if comm.isNumber(args[0], floatsAllowed=True):
                wait = float(args[0])
            else:
                return gn.error(calledFrom, "Invalid argument for time")
        
        time.sleep(wait)
        return 0
    
    except Exception as e:
        return gn.unknownErr(calledFrom, e)
