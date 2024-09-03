# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
import ctypes
import globalFile as gn

helpStr = """
Changes the title of the console window.
Syntax:
    TITLE [title]
Argument:
    title -> New title for the Second window.
"""

def TITLE(interpreter, args):
    "Changes the title of the console window."
    try:
        if args != '':
            ctypes.windll.kernel32.SetConsoleTitleW(args)
        else:
            ctypes.windll.kernel32.SetConsoleTitleW("Second 5")
        return 0
    except Exception as e: # If any error (I've never see any), then print it.
        return gn.unknownErr("title", e)
