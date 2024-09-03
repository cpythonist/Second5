# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License
# 

from bin import sexec

helpStr = """
Executes a string in the CPython interpreter.
Syntax:
    EXECUTE string1 [string2 ...]
Arguments:
    string<num> -> Strings to be executed in the CPython interpreter
"""

def EXECUTE(interpreter, args):
    "Executes a string in the CPython interpreter."
    return sexec.EXEC(interpreter, args)
