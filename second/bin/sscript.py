# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
import globalFile as gn
import intCommons as comm

helpStr = """
Runs a Second script.
Syntax:
    RUN script
Arguments:
    script -> Path of the Second script
"""

def SCRIPT(interpreter, args, calledFrom="script"):
    "Run a Second script."
    try:
        args, opts = comm.parse(args)
        if not args:
            return gn.error(calledFrom, "No script provided")
        if opts:
            return gn.error(calledFrom, f"Unknown option(s): {str(opts)[1:-1]}")
        
        for file in args:
            try:
                with open(file, 'r', buffering=1) as f:
                    for line in f:
                        # Executes the line in the interpreter
                        interpreter.onecmd(line)
            except FileNotFoundError:
                return gn.error(calledFrom, f"No such file: \"{file}\"")
        return 0

    except Exception as e:
        return gn.unknownErr(calledFrom, e)
