# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
from bin import ssleep

helpStr = """
Waits a certain amount of time before continuing.
Syntax:
    PAUSE time
Argument:
    time -> Time to wait in seconds
"""

def PAUSE(interpreter, args):
    "Waits a certain amount of time before continuing."
    return ssleep.SLEEP(interpreter, args, calledFrom="pause")
