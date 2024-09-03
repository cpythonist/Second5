# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
from bin import snew

helpStr = """
Creates a new file.
Syntax:
    TOUCH file
Argument:
    file -> Filename for the new file
"""

def TOUCH(interpreter, args):
    "Creates a new file."
    return snew.NEW(interpreter, args, calledFrom="touch")
