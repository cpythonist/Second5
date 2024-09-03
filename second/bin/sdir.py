# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
import os
import pathlib
import datetime   as dt
import globalFile as gn
import intCommons as comm

helpStr = """
Displays the contents one level inside a directory.
Syntax:
    DIR path1 [path2 ...]
Arguments:
    path<num> -> Directories which needs to be listed
"""

def singleDIR(path):
    "For single DIR commands (does not print the directory name first)."
    if os.path.isdir(path):
        path = str(path) + os.sep
        maxSize = 0
        files = False
        for j in os.scandir(path):
            files = True
            if len(str(j.stat().st_size)) > maxSize: maxSize = len(str(j.stat().st_size))
        
        gn.customPrint(f"  &&**{'DATE CREATED':<19}   {'DATE MODIFIED':<19}   TYPE   " + "{size:<{maximumSize}}   NAME##".format(size="SIZE", maximumSize=maxSize)) if files else None

        for i in os.scandir(path):
            typ = os.path.isfile(os.path.join(path, i.name))
            
            print("  {created}   {modified}   {typ}   {size:<{maximumSize}}   {name}".format(
                created = dt.datetime.fromtimestamp(os.path.getctime(os.path.join(path, i.name))).strftime(r'%d-%m-%Y %H:%M:%S'),
                modified = dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(path, i.name))).strftime(r'%d-%m-%Y %H:%M:%S'),
                typ = (gn.GREEN if gn.ANSI else '')+'FILE'+(gn.RESET if gn.ANSI else '') if typ else (gn.CYAN if gn.ANSI else '')+'DIR '+(gn.RESET if gn.ANSI else ''),
                size = (os.path.getsize(os.path.join(path, i.name)) if typ else '-'),
                maximumSize = maxSize,
                name = i.name
                )
            )
        return 0

    else:
        return gn.error("dir", f"No such directory: \"{path}\".")

def DIR(interpreter, args):
    "Displays the contents one level inside a directory."
    try:
        args, opts = comm.parse(args)
        if not opts:
            if not len(args):
                path = '.'
            elif len(args) == 1:
                path = args[0]
            else:
                path = args
        else:
            return gn.error("dir", f"Unknown option(s): {str(opts)[1:-1]}.")
        
        # Single directory, without printing directory name
        if len(args) < 2:
            return singleDIR(path)
        # Multiple directory(ies), printing directory name(s)
        else:
            err = 0
            for i in path:
                gn.info("dir", f"{gn.BOLD if gn.ANSI else ''}{gn.BLUE if gn.ANSI else ''}{pathlib.Path(i).resolve()}{gn.RESET if gn.ANSI else ''}:")
                # err will contain last reported error code
                temp = singleDIR(i)
                if temp != 0: err = temp
            return err
    
    except PermissionError:
        return gn.error("dir", "Access denied for the directory.")
    
    except OSError:
        return gn.error("dir", "The operation could not be performed. Possible reasons: invalid path, disc space issues")
        
    except Exception as e:
        return gn.unknownErr("dir", e)
