# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

import globalFile   as gn
import printStrings as ps

helpStr = """
Displays the startup string.
Syntax:
    INTRO
"""

def INTRO(interpreter, args):
    "Displays the startup string."
    try:
        gn.customPrint(ps.startString.lstrip('\n'))
        return 0
    except Exception as e:
        return gn.unknownErr("intro", e)
