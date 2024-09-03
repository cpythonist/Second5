# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 
# Same as COPY command
# 

# Imports
from bin import scopy

helpStr = """
Copies a file/directory to another directory.
Syntax:
    CP source dest
Arguments:
    source -> Path of source file/directory on the computer.
    dest   -> Destination directory for copying source into
"""

def CP(interpreter, args):
    "Copies a file/directory to another directory."
    return scopy.COPY(interpreter, args, calledFrom="cp")
