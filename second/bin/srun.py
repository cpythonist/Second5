# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
from bin import sscript


helpStr = """
Runs a Second script.
Syntax:
    RUN script
Arguments:
    script -> Path of the Second script
"""

def RUN(interpreter, args):
    "Run a Second script."
    return sscript.SCRIPT(interpreter, args, calledFrom="run")
