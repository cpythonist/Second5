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
Creates a new directory.
Syntax:
    MD name1 [name2 ...]
Arguments:
    name<num> -> Names of the new directories
"""

def MKDIR(interpreter, args, calledFrom="mkdir"):
    try:
        args, opts = comm.parse(args)
        if args:
            if opts:
                return gn.error(calledFrom, f"Unknown option(s) given: {str(opts)[1:-1]}")
            for name in args:
                os.makedirs(name)        
        else:
            return gn.error(calledFrom, f"Incorrect format")
        return 0
        
    except FileExistsError as e: # Directory exists
        return gn.error(calledFrom, f"File/Directory already exists: \"{pathlib.Path(name).resolve()}\"")
    
    except OSError: # Illegal character in directory name            
        return gn.error(calledFrom, f"Could not create directory. Possible reasons: Invalid character or the disc is full")
    
    except Exception as e:
        return gn.unknownErr(calledFrom, e)
