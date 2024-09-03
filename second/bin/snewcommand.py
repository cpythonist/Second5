# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
import os
import intCommons as comm
import globalFile as gn

helpStr = """
Create a new command for Second from a Python source file.
Syntax:
    NEWCOMMAND <name> <script>
Arguments:
    name   -> Name of the new command
    script -> Path of the Python source file
Structure of the script file:
<import-statements>
# Contains string for the specific command help
<var: helpString>
# Should return an integer for the error interpreter variable. 
# 0 for no error, 1 for recognised error, -1 for unrecognised error
<function: 
    uppercase-command-name,
    arguments:
        interpreter,
        args,
        calledFrom:
            If another command needs to call this function and print 
            separate names for errors and output
        other keyword arguments (positional arguments will most probably not work)
>
"""

def NEWCOMMAND(interpreter, args, calledFrom="newcommand"):
    "Create a new command for Second from a Python source file."
    try:
        args, opts = comm.parse(args)
        
        if len(args) != 2:
            return gn.error(calledFrom, "Incorrect format")
        if opts:
            return gn.error(calledFrom, f"Unknown option(s): {str(opts)[1:-1]}")
        
        def writeToFile(temp, args):
            with open(temp, 'w', buffering=1) as dest:
                with open(args[1], 'r', buffering=1) as src:
                    line = src.readline()
                    while line:
                        dest.write(line)
                        line = src.readline()
        
        if not (temp2:=os.path.isfile(temp:=(interpreter.accessPath + os.sep + "bin" + os.sep + 's' + args[0].lower() + '.py'))) and os.path.isfile(args[1]):
            writeToFile(temp, args)
        elif temp2 and os.path.isfile(args[1]):
            gn.error(calledFrom, f"Destination file for new command \"{args[0]}\" ({'s' + args[0] + '.py'}) exists. Overwrite [y]/n ? ", end='')
            choice = input().lower()
            if choice in ('', 'y', 'yes') or choice.isspace():
                writeToFile(temp, args)
            elif choice in ('n', 'no'):
                return 0
            else:
                return gn.error(calledFrom, "Invalid input; Operation terminated")
        else:
            return gn.error(calledFrom, f"Source file \"{args[1]}\" does not exist")
        
        return 0
    
    except OSError:
        return gn.error(calledFrom, "OS error. Possible reasons: invalid filename, disc space problems")
    
    except Exception as e:
        return gn.unknownErr(calledFrom, e)
