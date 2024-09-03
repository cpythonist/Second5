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
Displays a tree of all subdirectories (and files) inside a directory.
Syntax:
    TREE [dir] [-f]
Argument:
    dir -> Directory which needs to be examined.
Option:
    -f  -> Print files
"""

def TREE(interpreter, args):
    "Displays a tree of all subdirectories (and files) inside a directory."
    try:
        args, opts = comm.parse(args)
        # For printing files
        printFiles = False

        if len(args) == 1:
            args = args[0]
        elif not args:
            args = '.'
        else:
            return gn.error("tree", f"Incorrect format")
        
        if len(opts) == 1:
            # 'f' option is for printing files
            if opts[0] == 'f':
                printFiles = True
            else:
                return gn.error("tree", f"Unknown option: \"{opts[0]}\"")
        elif len(opts) > 1:
            return gn.error("tree", f"Unknown option(s): \"{str(opts)[1:-1]}\"")
        
        args      = str(pathlib.Path(args).resolve())
        count     = 0
        # Find the level of the directory in the file structure, as root variable in os.walk()
        # gives the full path of the directory being worked on
        levelArgs = args.count(os.sep)
        if not os.path.isdir(args):
            return gn.error("tree", f"No such directory: \"{args}\"")
        
        print(gn.CYAN + args + gn.RESET, end='')
        for root, dirs, files in os.walk(args):
            level = str(pathlib.Path(root).resolve()).count(os.sep) - levelArgs
            fillIndent = ' ' * 4 * (level-1) + ('-' * 2) + '>'
            print((f"{fillIndent} {gn.CYAN if gn.ANSI else ''}{os.path.basename(root)}{gn.RESET if gn.ANSI else ''}{os.sep}" if count else ''))
            fillSubindent = ' ' * 4 * (level) + '-' * 2 + '>'
            if printFiles:
                for file in files:
                    print(f"{fillSubindent} {gn.GREEN if gn.ANSI else ''}{os.path.basename(file)}{gn.RESET if gn.ANSI else ''}")
            count += 1
        
        return 0
        
    except FileNotFoundError:
        return gn.error("tree", "The directory was not found.")
    
    except Exception as e:
        return gn.unknownErr("tree", e)
