# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Licensed under the Apache-2.0 License.
# 
# Originally, this feature was written in default method of this class, so that commands that 
# are not present in Second 5 could be executed as terminal commands. But this was later removed 
# to prevent accidental execution of terminal commands, and thus a new command called COMMAND was 
# created in Second 5 to accomodate the feature.
# 

# Imports
import ctypes
import os
import globalFile as gn

helpStr = """
Runs terminal commands on Second.
Syntax:
    COMMAND command
Argument:
    command -> Command to execute in terminal
"""

def COMMAND(interpreter, args:str):
    "Executes terminal commands."
    try:
        gn.info("command", "Terminal output:")
        os.system(args)
        # Title changes when terminal commands are executed, so to revert title to title of interpreter
        ctypes.windll.kernel32.SetConsoleTitleW(interpreter.title)
        return 0
    # Never observed
    except Exception as e:
        return gn.unknownErr("command", e)
