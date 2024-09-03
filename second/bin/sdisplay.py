# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
import os
import pathlib
import sys
import globalFile as gn
import intCommons as comm

helpStr = """
Displays the contents of a text file.
Syntax:
    DISPLAY file
Argument:
    file -> File to be displayed
Option:
    -i   -> Display file information
"""

def DISPLAY(interpreter, args, calledFrom="display"):
    "Displays the contents of a text file."
    try:
        # For error reporting
        argsErrorReporting = args
        args, opts         = comm.parse(args)
        info               = False

        if not (len(args) == 1 or opts):
            return gn.error(calledFrom, f"Incorrect format")
        elif len(args) == 1 and opts:
            if len(opts) == 1:
                # 'i' option is for displaying file information
                if opts[0] == 'i':
                    info = True
                else:
                    return gn.error(calledFrom, f"Unknown option: \"{opts[0]}\"")
            else:
                return gn.error(calledFrom, f"Too many options: {str(opts)[1:-1]}")
        
        args = args[0]
        # Display file information if variable info is True
        gn.info(calledFrom, f"{gn.BOLD if gn.ANSI else ''}{gn.GREEN if gn.ANSI else ''}File:{gn.RESET if gn.ANSI else ''} \
\"{pathlib.Path(args).resolve()}\"\n{gn.BOLD if gn.ANSI else ''}{gn.GREEN if gn.ANSI else ''}Size:{gn.RESET if gn.ANSI else ''} \
 {os.path.getsize(args)} B") if info else None

        # Write the file to stdout
        with open(args, 'r', buffering=4096) as f:
            for line in f:
                sys.stdout.write(line)
            print()
        
        return 0
        
    except FileNotFoundError as e:
        return gn.error(calledFrom, f"No such file: \"{argsErrorReporting}\"")
    
    except PermissionError:
        return gn.error(calledFrom, f"\"{pathlib.Path(argsErrorReporting).resolve()}\": Is a directory or access is denied")
    
    except OSError:
        return gn.error(calledFrom, f"\"{pathlib.Path(argsErrorReporting).resolve()}\": Invalid path")
    
    except Exception as e:
        return gn.unknownErr(calledFrom, e)
