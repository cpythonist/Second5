# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
from bin import sfile

helpStr = """
Displays the type of a path (file or directory).
Syntax:
    TYPE path1 [path2 ...] [-h<0,1,2,3>]
Arguments:
    path<num> -> Paths to be examined
Options:
    -h<0,1,2,3> -> "Human-readable" memory values
                    (0: bytes, 1: kilobytes, 2: megabytes, 3: gigabytes)
"""

def TYPE(interpreter, args):
    "Displays the type of a path (file or directory)."
    return sfile.FILE(interpreter, args, calledFrom="type")
