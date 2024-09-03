# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
from bin import sdel

helpStr = """
Removes a file/directory.
Syntax:
    REMOVE path1 [path2 ...]
Arguments:
    path<num> -> Paths of files/directories to be removed.
"""

def RM(interpreter, args):
    "Removes a file/directory."
    return sdel.DEL(interpreter, args, calledFrom="rm")
