# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
import os
import shutil
import globalFile as gn
import intCommons as comm

helpStr = """
Deletes a file/directory.
Syntax:
    DEL path1 [path2 ...]
Arguments:
    path<num> -> Path of file/directory to be deleted
"""

def DEL(interpreter, args, calledFrom="del"):
    "Deletes a file/directory."
    try:
        args, opts = comm.parse(args)
        if not args:
            return gn.error(calledFrom, "Incorrect format.")
        if not opts:
            recurse = False
        elif len(opts) == 1:
            if 'r' == opts[0]:
                recurse = True
            else:
                return gn.error(calledFrom, f"Unknown option: \"{opts[0]}\".")
        else:
            return gn.error(calledFrom, f"Too many options: {str(opts)[1:-1]}.")
        
        for path in args:
            try:
                if os.path.isfile(path):
                    os.remove(path)
                # If it a directory, remove according to variable recurse
                elif os.path.isdir(path):
                    if recurse:
                        shutil.rmtree(path)
                    else:
                        for i in os.scandir(path):
                            if os.path.isdir(i):
                                continue
                            os.remove(i)
                else:
                    return gn.error(calledFrom, f"No such file or directory: \"{path}\".")
            
            except PermissionError:
                return gn.error(calledFrom, f"Access is denied for \"{path}\"")
            
            except FileNotFoundError:
                return gn.error(calledFrom, f"No such file or directory: \"{path}\"")
            
            except OSError:
                return gn.error(calledFrom, f"The OS could not perform the operation for \"{path}\"")    

    except Exception as e:
        return gn.unknownErr(calledFrom, e)
