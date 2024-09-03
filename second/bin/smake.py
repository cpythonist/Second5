# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
from bin import snewcommand

helpStr = """
Create a new command for Second from a Python source file.
Syntax:
    MAKE <name> <script>
Arguments:
    name   -> Name of the new command
    script -> Path of the Python source file
Structure of the script file:
<import-statements>
# Contains string for the specific command help
<var: helpString>
# Should return an integer for the error interpreter variable. 
# 0 for no error, 1 for recognised error, -1 for unrecognised error
<function: 
    uppercase-command-name,
    arguments:
        interpreter,
        args,
        calledFrom:
            If another command needs to call this function and print 
            separate names for errors and output
        other keyword arguments (positional arguments will most probably not work)
>
"""

def MAKE(interpreter, args):
    "Create a new command for Second from a Python source file."
    return snewcommand.NEWCOMMAND(interpreter, args, calledFrom="make")
