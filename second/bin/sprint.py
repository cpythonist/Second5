# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
from bin import sdisplay


helpStr = """
Displays the contents of a text file.
Syntax:
    PRINT file
Argument:
    file -> Path of the text file
"""

def PRINT(interpreter, args):
    "Displays the contents of a text file."
    return sdisplay.DISPLAY(interpreter, args, calledFrom="print")
