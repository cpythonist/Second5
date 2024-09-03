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
Lists the contents of the specified directory.
Syntax:
    LS [path1 path2 ...] [-l]
Arguments:
    path<num> -> Directories to list the contents of. Defaults to current working directory
Option:
    -l   -> Long listing format
"""

def singleLS(path, llong):
    "Single directory listing, without printing directory path."
    # llong is for determining if long listing is to be done
    if os.path.isdir(path):
        if llong:
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
        else:
            maxLen = 0
            for j in os.scandir(path):
                maxLen = max(maxLen, len(j.name))
            
            count = 0
            if maxLen > 0:
                perLine = os.get_terminal_size().columns // maxLen
            else:
                return 1
            
            if not perLine: perLine = 1
            print('  ', end='')
            for i in os.scandir(path):
                if (not (count % perLine)) and count:
                    print("\n  ", end='')
                if ' ' not in i.name:
                    print(((gn.GREEN if os.path.isfile(i) else gn.CYAN) if gn.ANSI else '') + i.name + (gn.RESET if gn.ANSI else ''), end='    ')
                else:
                    print(f"{(gn.GREEN if os.path.isfile(i) else gn.CYAN) if gn.ANSI else ''}\"" + i.name + f'"{gn.RESET if gn.ANSI else ""}', end='    ')
                count += 1
            print()

        return 0
    
    else:
        return gn.error("ls", f"No such directory: \"{path}\"")

def LS(interpreter, args):
    "Lists the contents of the specified directory."
    try:
        # llong is for determining if long listing is to be done
        args, opts = comm.parse(args)
        llong      = False

        if not args:
            path = '.'
        elif len(args) == 1:
            path = args[0]
        else:
            path = args
        
        if not opts:
            pass
        elif len(opts) == 1:
            if opts[0] == 'l':
                llong = True
            else:
                return gn.error("ls", f"Unknown option: \"{opts[0]}\".")
        else:
            return gn.error("ls", f"Too many options: {str(opts)[1:-1]}.")

        if len(args) < 2:
            return singleLS(path+os.sep, llong)
        else:
            # Multiple paths given
            err = 0
            for i in path:
                gn.customPrint(f"&&{pathlib.Path(i).resolve()}:")
                temp = singleLS(i+os.sep, llong)
                if temp != 0: err = temp
            return err

    except Exception as e:
        return gn.unknownErr("ls", e)
