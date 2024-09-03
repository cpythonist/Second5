# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
import os
import pathlib
import globalFile as gn
import intCommons as comm

helpStr = """
Creates a new file.
Syntax:
    FILE name
Argument:
    name -> File name for the new file
"""

def NEW(interpreter, args, calledFrom="new"):
    "Creates a new file."
    try:
        args, opts = comm.parse(args)
        err = False

        if not args:
            return gn.error(calledFrom, "Incorrect format")
        
        if opts:
            return gn.error(calledFrom, f"Unknown option(s): {str(opts)[1:-1]}")
        
        if len(args) == 1:
            if os.path.isfile(args[0]):
                gn.error(calledFrom, f"File/Directory already exists: \"{pathlib.Path(args[0]).resolve()}\"")
            else:
                try:
                    open(args[0], 'w').close()
                except PermissionError:
                    gn.error(calledFrom, "File/Directory with the same name already exists or access is denied to create file.")
                    return 1
        
        else:
            for path in args:
                if os.path.isfile(path):
                    gn.error(calledFrom, f"File/Directory already exists: \"{pathlib.Path(path).resolve()}\"")
                else:
                    try:
                        open(path, 'w').close()
                    except PermissionError:
                        gn.error(calledFrom, f"File/Directory already exists or access is denied to create file(s): \"{path}\"")
                        err = True
            
            if err:
                return 1
        
        return 0
    
    except OSError:
        return gn.error(calledFrom, "OS error. Possible reasons: invalid filename, disc space problems")

    except Exception as e:
        return gn.unknownErr(calledFrom, e)
