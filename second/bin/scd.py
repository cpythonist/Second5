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
Changes the current working directory.
Syntax:
    CD path
Argument:
    path -> Directory to change to
"""

def CD(interpreter, args):
    "Changes the current working directory."
    try:
        args, opts = comm.parse(args)

        if len(args) == 1 and not opts:
            # '*' is like '~' behaviour of Linux; '>' and '<' are like '-' behaviour of Linux; '?' is like 'pwd', for
            # getting the current working directory
            args = args[0].replace('*', os.path.expanduser("~"))
            
            # This is for users trying to navigate back to the directory they were previously in the drive, before
            # changing to another drive (like in cmd.exe). For example, if the user is in their home directory 
            # (C:\Users\<user>\) and had changed from this directory to some other drive, say "D:\", and to come 
            # back to same directory in "C:\" drive, the command would be "cd C:?"
            if len(args) > 1 and args.endswith('?'):
                os.chdir(args[:-1])
            
            # os.sep is added to the argument because using '\' and the end of the prompt actually continues 
            # the prompt, and the root drive couldn't be achieved with the actual path of the drive.
            elif os.path.isdir(args + os.sep):
                interpreter.oldCDPath = os.getcwd()
                os.chdir(args + os.sep)
            
            elif args in ('<', '>'):
                tempOldCDPath = os.getcwd()
                os.chdir(interpreter.oldCDPath)
                interpreter.oldCDPath = tempOldCDPath
            
            elif args == '?':
                gn.customPrint(os.getcwd())
            
            else:
                return gn.error("cd", f"Directory \"{args}\" not found")
        
        # Use without argument changes the CWD to user directory
        elif not len(args):
            interpreter.oldCDPath = os.getcwd()
            os.chdir(os.path.expanduser("~"))
        
        else:
            return gn.error("cd", "Incorrect format")
    
        return 0
    
    except PermissionError:
        return gn.error("cd", f"Access is denied: \"{args}\"")
    
    except OSError:
        return gn.error("cd", f"\"{args}\": Invalid argument. Possible reason: invalid path")
    
    except Exception as e:
        return gn.unknownErr("cd", e)
