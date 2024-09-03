# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License
# 

# Imports
import globalFile as gn
import intCommons as comm

helpStr = """
Echoes a string or writes a string to a file.
Syntax:
    ECHO string [file] [-o]
Arguments:
    string -> String to be echoed
    file   -> Path of file to be written (appended if file exists)
Options:
    -o     -> Overwrite file, if it exists
    -s     -> Write string to stdout
"""

def ECHO(interpreter, args):
    "Echoes a string or writes a string to a file."
    try:
        args, opts = comm.parse(args)
        append = True
        if len(args) == 1:
            string, path = args[0], None
        elif len(args) == 2:
            string, path = args[0], args[1]
        elif len(args) == 0:
            string, path = '', None
        else:
            return gn.error("echo", "Incorrect format.")
        
        if not opts:
            append = True
            if path == None:
                stdout = True
            else:
                stdout = False
        
        elif len(opts) == 1:
            if opts[0] == 'o' and len(args) == 2:
                append = False
                stdout = False
            elif opts[0] == 's':
                stdout = True
            else:
                return gn.error("echo", f"Unknown option: \"{opts[0]}\".")
        
        elif len(opts) == 2:
            if sorted(opts) == ['o', 's']:
                append = False
                stdout = True
            else:
                return gn.error("echo", f"Unknown option(s): {str(opts)[1:-1]}.")
        
        else:
            return gn.error("echo", f"Too many options: {str(opts)[1:-1]}.")

        if path:
            with open(path, 'a' if append else 'w', buffering=1) as f:
                f.write(string)
            
        if stdout:
            prevWasAnEscChar = False
            for i, char in enumerate(string):
                try:
                    if (char == 'n' or char == '\\') and prevWasAnEscChar:
                        prevWasAnEscChar = False
                        continue
                    
                    if char == '\\' and ((temp:=(string[i+1] == 'n')) or (string[i+1] == '\\')):
                        print('\n' if temp else '\\', end='')
                        prevWasAnEscChar = True
                    else:
                        print(char, end='')
                
                except IndexError:
                    print(char, end='')
            print()

        return 0
    
    except OSError:
        return gn.error("echo", "Invalid argument(s) or another file/folder with the same name exists.")
    
    except Exception as e:
        return gn.unknownErr("echo", e)
