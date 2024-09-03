# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
import shutil
import globalFile as gn
import intCommons as comm

helpStr = """
Moves a file or directory from one location to another, or renames the file/directory.
Syntax:
    MOVE src dest
Arguments:
    src   -> Source file or directory
    dest  -> Destination file or directory
"""

def MOVE(interpreter, args, calledFrom="move"):
    "Moves a file or directory from one location to another, or renames the file/directory."
    try:
        args, opts = comm.parse(args)
        if len(args) == 2:
            if not opts:
                src, dest = args
            else:
                return gn.error(calledFrom, f"Unknown option(s): {str(opts)[1:-1]}")
        else:
            return gn.error(calledFrom, f"Incorrect format")
        shutil.move(src, dest)
        return 0
    
    except FileNotFoundError:
        return gn.error(calledFrom, f"No such source file or directory: \"{src}\"")
    
    except Exception as e:
        return gn.unknownErr(calledFrom, e)
