# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
from bin import smkdir

helpStr = """
Creates a new directory.
Syntax:
    MD name1 [name2 ...]
Arguments:
    name<num> -> Names of the new directories
"""
def MD(interpreter, args):
    "Creates a new directory."
    return smkdir.MKDIR(interpreter, args, calledFrom="md")
