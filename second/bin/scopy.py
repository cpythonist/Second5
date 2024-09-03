# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
import os
import pathlib
import shutil
import globalFile as gn
import intCommons as comm

helpStr = """
Copies a file/directory to another directory.
Syntax:
    COPY source dest
Arguments:
    source -> Path of source file/directory on the computer
    dest   -> Destination directory for copying source into
"""

def COPY(interpreter, args, calledFrom="copy"):
    "Copies a file/directory to another directory."
    try:
        args, opts = comm.parse(args)
        srcTyp = None

        if len(args) == 2:
            if not opts:
                src, dest = args
            else:
                return gn.error(calledFrom, f"Unknown option(s): {str(opts)[1:-1]}")
        else:
            return gn.error(calledFrom, f"Incorrect format.")
        
        # Check if source file or directory exists. os.path.exists() is not used because, type of the source given was needed
        # (file or directory).
        if (temp:=os.path.isfile(src)) or os.path.isdir(src):
            src = str(pathlib.Path(src).resolve())
            srcTyp = 'File' if temp else 'Directory'
        else:
            return gn.error(calledFrom, f"No such source file or directory: \"{src}\".")

        # Destination file/directory already exists
        if os.path.isdir(dest) and not os.path.isfile(src):
            dest = str(pathlib.Path(dest).resolve())
            gn.info(calledFrom, f"{srcTyp} {dest} exists. Do you want to overwrite it? [y]/n ?\n$ ", end='', printFunc=True)

            overwrite = input().lower()
            if overwrite in ('', 'y', 'yes') or overwrite.isspace():
                pass
            elif overwrite in ('n', 'no'):
                return 2
            else:
                return gn.error(calledFrom, "Invalid input")
        
        else:
            os.makedirs(dest)

        # Copy file/directory
        if srcTyp == 'File':
            shutil.copy2(src, dest)
        elif srcTyp == 'Firectory':
            shutil.copytree(src, dest, symlinks=True, dirs_exist_ok=True)
        
        return 0
    
    except OSError:
        return gn.error(calledFrom, "The OS could not perform the operation. Possible reasons: invalid path or access is denied")
    
    # Process stopped in between, like during overwrite input
    except EOFError:
        return 2

    except Exception as e:
        return gn.unknownErr(calledFrom, e)
