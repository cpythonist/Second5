# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
import os
import pickle
import globalFile as gn
import intCommons as comm

helpStr = """
Changes the prompt variable of the program.
Syntax:
    PROMPT [prompt] [-w] [-r]
Argument:
    prompt -> New prompt for Second
              %U - Username
              %S - OS name
              %R - Release number
              %P - Path (current working directory)
              %% - Percentage sign
Options:
    -w     -> Write prompt variable to file 'ssettings.dat'
    -r     -> Read prompt variable from file 'ssettings.dat'
Note: If the program is running in a terminal WITHOUT ANSI support, ANSI escape codes are removed from the given data to the PROMPT command.
"""

def PROMPT(interpreter, args):
    try:
        args, opts = comm.parse(args)

        # If no arguments, restore original prompt of the program
        if not args:
            interpreter.realPrompt = f"{gn.BLUE}%U{gn.RESET}->{gn.BLUE}%S%R{gn.RESET}&&{gn.GREEN}%P{gn.RESET}(S5):\n{gn.GREEN}${gn.RESET} "
        elif len(args) == 1:
            interpreter.realPrompt = args[0]
        else:
            return gn.error("prompt", f"Too many arguments: {str(args)[1:-1]}.")
        
        if not len(opts):
            # Work is done, no writing to 'ssettings.dat' needed, temporary prompt change
            return 0
        elif len(opts) == 1:
            # 'w' option is for writing the prompt value to file 'ssettings.dat'
            if opts[0] == 'w':
                with open(os.path.join(f"{interpreter.accessPath}", "ssettings.dat"), 'rb+') as f:
                    data = pickle.load(f)
                data["prompt"] = interpreter.realPrompt
                with open(os.path.join(f"{interpreter.accessPath}", "ssettings.dat"), 'wb') as f:
                    pickle.dump(data, f)
            # 'r' option is for reading the prompt value from file 'ssettings.dat'
            elif opts[0] == 'r':
                gn.info("prompt", repr(interpreter.realPrompt))
            else:
                return gn.error("prompt", f"Unknown option: \'{opts[0]}\'")
        else:
            return gn.error("prompt", f"Too many options: {str(opts)[1:-1]}")
        return 0
        
    except FileNotFoundError:
        gn.error("prompt", "\'ssettings.dat\': Not found")
        gn.info("prompt", "Prompt variable will be temporarily changed. Please restart the program", printFunc=True)
        return 3
    
    except (pickle.UnpicklingError, KeyError):
        gn.error("prompt", "\'ssettings.dat\': Empty/Invalid data")
        gn.info("prompt", "Prompt variable will be temporarily changed. Please restart the program", printFunc=True)
        return 3
    
    except PermissionError:
        gn.error("prompt", "\'ssettings.dat\': Access is denied")
        gn.info("prompt", "Prompt variable will be temporarily changed. Please restart the program", printFunc=True)
        return 3
    
    except Exception as e:
        return gn.unknownErr("prompt", e)
