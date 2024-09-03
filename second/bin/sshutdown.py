# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
import subprocess
import globalFile as gn
import intCommons as comm

helpStr = """
Shuts down the computer.
Syntax:
    SHUTDOWN options
Options:
    -s - Shutdown the computer.
    -r - Restart the computer.
    -t - Set wait period for the SHUTDOWN operation.
    -h - Enables hybrid mode while startup.
If no option is used or only '-h' and/or '-t' options are used, then by default '-s' argument will be executed.
"""

def SHUTDOWN(interpreter, args):
    "Shuts down the computer."
    try:
        args, opts = comm.parse(args)
        command    = ["shutdown"]

        for i in opts:
            # Add necessary options
            if i == '-s':
                command.append("/s")
            elif i == '-r':
                command.append("/r")
            elif i.startswith('-t') and i[1:].isnumeric():
                command.append(f"/t {int(i[1:]):03d}")
            elif i == '-h':
                command.append("/hybrid")
            else:
                return gn.error("shutdown", f"Unknown option: \"{i}\".")
        
        # If no shutdown or restart option is specified, then by default '-s' argument will be executed
        if ('-s' not in command) and ('-r' not in command):
            command.append("/s")
        subprocess.run(command)
        return 0
    
    # Never observed
    except Exception as e:
        return gn.unknownErr("shutdown", e)
