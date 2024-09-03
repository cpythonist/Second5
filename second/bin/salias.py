# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
import shutil
import os
import globalFile as gn
import intCommons as comm

helpStr = """
Aliases a command.
Syntax:
    ALIAS [name command]
Arguments:
    name    -> Name of the alias
    command -> Command to be aliased
"""

def ALIAS(interpreter, args):
    "Alias a command."
    try:
        args, opts = comm.parse(args)
        if opts:
            return gn.error("alias", f"Unknown option(s): {str(opts)[1:-1]}")
        
        def isAliasPresent(word, line):
            "Check if alias name is already present"
            for i in range(len(line)):
                if line[i] == '=':
                    break
            if line[:i] == word:
                return True
            return False
        
        # If no argument is provided, print all aliases
        if not args:
            with open(interpreter.accessPath + os.sep + f"saliases.txt", 'r', buffering=1) as f:
                for line in f:
                    print(line, end='')
        
        # One argument is given, print that particular alias
        elif len(args) == 1:
            with open(interpreter.accessPath + os.sep + f"saliases.txt", 'r', buffering=1) as f:
                for line in f:
                    if isAliasPresent(args[0], line):
                        print(line, end='')
                        break
                else:
                    return gn.error("alias", f"No such alias: '{args[0]}'")
        
        # Two arguments, create an alias
        elif len(args) == 2:
            # Value found[1] is used for storing line number of first occurance of given alias (if it already exists)
            found = False, -1
            aliasTextFile = f"{interpreter.accessPath}{os.sep}saliases.txt"
            aliasTempFile = f"{interpreter.accessPath}{os.sep}bin{os.sep}saliases.temp"

            # Try to locate alias if it already exists
            with open(aliasTextFile, 'r', buffering=1) as f:
                for j, line in enumerate(f):
                    for i, char in enumerate(line):
                        # If character is '=', indicates end of alias name
                        if char == '=':
                            break
                    if args[0] == line[:i]:
                        found = True, j
                        break
            
            # If alias already exists, update it
            if found[0]:
                # Make temporary file by copying original file.
                # Open temporary file for reading and original file for writing, and copy lines from temporary file to original 
                # file except the line with alias name, where alias will be inserted instead, with the data from arguments.
                shutil.copyfile(aliasTextFile, aliasTempFile)
                with open(aliasTempFile, 'r', buffering=1) as f1:
                    with open(aliasTextFile, 'w', buffering=1) as f:
                        for i, line in enumerate(f1):
                            if i != found[1]:
                                f.write(line)
                            else:
                                f.write(f"{args[0]}={args[1]}\n")
                os.remove(aliasTempFile)
            
            # Else create a new alias
            else:
                # Open in append mode (cursor at end of file)
                with open(aliasTextFile, 'a+', buffering=1) as f:
                    # For checking if previous character is '\n', otherwise to insert a newline
                    pos = f.tell()
                    if pos != 0:
                        f.seek(pos - 1)
                        prevChar = f.read(1)
                        f.seek(pos)
                    else:
                        prevChar = '\n'
                    
                    if prevChar == '\n':
                        f.write(f"{args[0]}={args[1]}\n")
                    else:
                        f.write(f"\n{args[0]}={args[1]}\n")
        
        # More than three arguments, error
        else:
            return gn.error("alias", "Incorrect format")
        
        return 0
    
    except PermissionError:
        return gn.error("alias", "Access is denied.")

    except Exception as e:
        import traceback
        traceback.print_exc()
        return gn.unknownErr("alias", e)
