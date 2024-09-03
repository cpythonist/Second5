# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
import datetime as dt
import globalFile as gn

helpStr = """
Displays the current system date.
Syntax:
    DATE
"""

def DATE(interpreter, args):
    "Displays the current system date."
    try:
        gn.info("date", f"Date today: {dt.datetime.today().strftime('%d.%m.%Y (%d %B %Y)')} (dd.mm.yyyy).")
        return 0
    except Exception as e:
        return gn.unknownErr("date", e)
