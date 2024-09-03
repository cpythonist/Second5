# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
import os
import intCommons as comm
import globalFile as gn

helpStr = """
Starts a file, directory or executable.
Syntax:
    START name [-a]
Argument:
    name -> Path of file/directory, name of a program added to the PATH variable or a webpage
Option:
    -a   -> Run as an administrator
"""

def START(interpreter, args):
    "Starts a file, directory or executable."
    try:
        args, opts = comm.parse(args)
        
        if len(args) == 1:
            args = args[0]
            # No options, indicates run as same user
            if not opts:
                isAdminMode = False
            elif len(opts) == 1:
                # 'a' option, indicates run as admin
                if opts[0] == 'a':
                    isAdminMode = True
                else:
                    return gn.error("start", f"Unknown option: \"{opts[0]}\"")
            else:
                return gn.error("start", f"Too many options: {str(opts)[1:-1]}")
        else:
            return gn.error("start", "Incorrect format")
        
        os.startfile(args, 'runas') if isAdminMode else os.startfile(args)
        return 0
        
    except FileNotFoundError as e:
        return gn.error("start", f"\"{args}\": Is not a file, directory or webpage")
    
    except OSError as e:
        return gn.error("start", "OS error. Possible reasons: The process was aborted by the user or the path is inaccessible")
        
    except Exception as e:
        return gn.unknownErr("start", e)
