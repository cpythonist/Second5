# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
from bin import smove

helpStr = """
Moves a file or directory from one location to another, or renames the file/directory.
Syntax:
    MV src dest
Arguments:
    src   -> Source file or directory
    dest  -> Destination file or directory
"""

def MV(interpreter, args):
    "Moves a file or directory from one location to another, or renames the file/directory."
    return smove.MOVE(interpreter, args, calledFrom="mv")
