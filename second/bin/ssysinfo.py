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
Displays the system information.
Syntax:
    SYSINFO [-c]
Option:
    -c -> Copies command output to clipboard
"""

def SYSINFO(interpreter, args):
    "Displays the system information."
    try:
        args, opts = comm.parse(args)
        
        if not args:
            # No options, just display the sysinfo
            if not opts:
                copy = False
            elif len(opts) == 1:
                # 'c' option provided, copy output to clipboard
                if opts[0] == 'c':
                    copy = True
                else:
                    return gn.error("sysinfo", f"Unknown option: \"{opts[0]}\".")
            else:
                return gn.error("sysinfo", f"Too many options: \"{str(opts)[1:-1]}\".")
        else:
            return gn.error("sysinfo", f"Unknown argument(s): \"{str(args)[1:-1]}\".")

        if not copy:
            comm.printSysinfo(copy=False)
        else:
            # comm.printSysinfo() returns the unformatted string when argument copy is set to True
            copyStr = comm.printSysinfo(copy=True)
            subprocess.run(["clip.exe"], input=''.join(copyStr).encode("utf-8"), check=True)
        return 0

    except Exception as e:
        return gn.unknownErr("sysinfo", e)
