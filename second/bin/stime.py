# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
import datetime   as dt
import globalFile as gn

helpStr = """
Displays the current system time.
Syntax:
    TIME
"""

def TIME(interpreter, args):
    "Displays the current system time."
    try:
        gn.info("time", f"Time now is: {dt.datetime.now().strftime('%H:%M.%S [%f]')} (hh:mm.ss [microseconds]).")
        return 0
    except Exception as e:
        return gn.unknownErr("time", e)
