# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License
# 

import mimetypes
import os
import pathlib
import globalFile as gn
import intCommons as comm

helpStr = """
Displays the type of a path (file or directory).
Syntax:
    FILE path1 [path2 ...] [-h<0,1,2,3>]
Arguments:
    path<num> -> Paths to be examined
Options:
    -h<0,1,2,3> -> "Human-readable" memory values
                    (0: bytes, 1: kilobytes, 2: megabytes, 3: gigabytes)
"""

def FILE(interpreter, args, calledFrom="file"):
    "Displays the type of a path (file or directory)."
    try:
        args, opts = comm.parse(args)
        num = 0
        if len(args) == 0:
            return gn.error(calledFrom, "Incorrect format")
        if len(opts) < 2:
            # 'h' option is for "human-readable" memory size formatting
            if opts:
                if opts[0][0] != 'h':
                    return gn.error(calledFrom, f"Unknown option: \'{opts[0]}\'")
                # Check if number after 'h' option is nothing, 0, 1, 2 or 3
                if (temp:=opts[0][1:]) and temp in ('', '0', '1', '2', '3'):
                    if not temp:
                        temp = '0'
                    # Convert the number to integer for dividing file size with it
                    num = int(temp)
                else:
                    return gn.error(calledFrom, f"Unknown option: \'{opts[0]}\'")
        
        # Assign file size prefixes
        for i in range(0, 4):
            if num == i:
                alpha = ('', 'k', 'M', 'G')[num]
        
        def printFileTyp(givenFileOrDir, printNames=False):
            "For printing one path information, with/without printing its path, based on argument printNames."
            try:
                # Get type of the file
                typ = mimetypes.guess_type(givenFileOrDir)

                if os.path.isfile(givenFileOrDir):
                    temp = typ[0] if typ[0] is not None else "unknown"
                elif os.path.isdir(givenFileOrDir):
                    temp = "directory"
                else:
                    # Will be caught in try..except statement
                    raise FileNotFoundError
                
                # Print information with path if argument printNames is True else omit path
                print(pathlib.Path(givenFileOrDir).resolve()) if printNames else None
                gn.customPrint(f"{'   ' if printNames else ''}\
{temp}  Encoding: {typ[1] if typ[1] is not None else '-'}\n{'   ' if printNames else ''}\
Size: {str(os.path.getsize(givenFileOrDir)/(10**num)) + ' ' + alpha + "B" if temp != "directory" else '-'}")
                
                return 0
            
            except FileNotFoundError:
                return gn.error(calledFrom, f"No such file/directory: {givenFileOrDir}")
            
            except PermissionError:
                return gn.error(calledFrom, f"Access is denied: {givenFileOrDir}")
            
            except OSError:
                return gn.error(calledFrom, f"OS error: Unknown causes. Possible reasons: file/directory name is incorrect or access is denied.")
        
        returnVal = 0

        if len(args) == 1:
            returnVal = printFileTyp(args[0])
        else:
            for i in args:
                if (temp:=printFileTyp(i, printNames=True)) != 0:
                    # returnVal will be last returned error code
                    returnVal = temp

        return returnVal
    
    except Exception as e:
        return gn.unknownErr(calledFrom, e)
