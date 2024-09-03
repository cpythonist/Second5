# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
from bin import sdel

helpStr = """
Deletes a file/directory.
Syntax:
    DELETE path1 [path2 ...]
Arguments:
    path<num> -> Path of file/directory to be deleted
"""

def DELETE(interpreter, args):
    "Deletes a file/directory."
    return sdel.DEL(interpreter, args, calledFrom="delete")
