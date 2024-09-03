# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# 

# Imports
import subprocess
import globalFile as gn
import intCommons as comm

helpStr = """
Kills the specified process(es).
Syntax:
    KILL process1 [process2 ...] [-p] [-f] [-c]
Arguments:
    process<num> -> Process name or process ID to be killed
Options:
    -p           -> Kill the process with its process ID
    -f           -> Kill the process forcefully
    -c           -> Kill the process and all of its child processes
"""

def KILL(interpreter, args):
    "Kills the specified process(es)."
    try:
        args, opts = comm.parse(args)
        # Variable call holds the command to be called with subprocess.run() in a list
        call = ["taskkill"]

        if not args:
            return gn.error("kill", f"Incorrect format")
        if (not opts) or ('p' not in opts):
            call.append("/im")
        else:
            call.append("/pid")
        
        if len(opts) in (0,1,2,3):
            for opt in opts:
                if opt == 'c':
                    call.append("/t")
                elif opt == 'f':
                    call.append("/f")
                elif opt == 'p':
                    pass
                else:
                    return gn.error("kill", f"Invalid option: \"{opt}\"")
        else:
            return gn.error("kill", f"Too many options: {str(opts)[1:-1]}")

        # Variable call2 holds the command to be called with subprocess.run() in a list, with process name or PID at index 2
        call2 = list(call)
        for proc in args:
            call2.insert(2, proc)
            result = subprocess.run(call2, capture_output=True)
            if not (result.stderr == b''):
                # Will be caught in the except block
                raise subprocess.CalledProcessError(-1, proc)
        return 0
        
    except subprocess.CalledProcessError as e:
        return gn.error("kill", f"Process{'' if call[1] == '/im' else ' PID'} \"{e.cmd}\" could either be not terminated (completely) or was not found")
        
    except Exception as e:
        return gn.unknownErr("kill", e)
