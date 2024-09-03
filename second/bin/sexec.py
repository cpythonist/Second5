# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License
# 

import traceback
import globalFile as gn
import intCommons as comm

helpStr = """
Executes a string in the CPython interpreter.
Syntax:
    EXEC string1 [string2 ...]
Arguments:
    string<num> -> Strings to be executed in the CPython interpreter
"""

def EXEC(interpreter, args):
    "Executes a string in the CPython interpreter."
    try:
        args, opts = comm.parse(args)
        if not args:
            return gn.error("exec", "Incorrect format.")
        if opts:
            return gn.error("exec", f"Unknown option(s): {str(opts)[1:-1]}")
        
        for code in args:
            try:
                exec(code)
            except:
                for i, line in enumerate(traceback.format_exc().splitlines()):
                    gn.customPrint(line) if i > 7 else None
    
    except Exception as e:
        return gn.unknownErr("exec", e)
