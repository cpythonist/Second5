# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

# Imports
import globalFile as gn
import intCommons as comm

helpStr = """
Searches for a substring in a string given.
Syntax:
    FIND substring string [-c]
Arguments:
    substring -> Substring to be searched in <string>
    string    -> String to be searched in
Option:
    -c        -> Case-sensitive search
"""

def FIND(interpreter, args):
    "Searches for a substring in a string given."
    try:
        args, opts = comm.parse(args)
        if len(args) != 2:
            return gn.error("find", f"Incorrect format")
        
        substring, string = args
        caseSen           = False

        if len(opts) == 1:
            if opts[0] != 'c':
                return gn.error("find", f"Unknown option: \'{opts[0]}\'")
            caseSen = True
        elif opts:
            return gn.error("find", f"Too many options: {str(opts)[1:-1]}")
        
        gn.info("find", f"Searching for \"{substring}\" in \"{string}\" {'(case-sensitive)' if caseSen else '(case-INsensitive)'}:")
        old   = 0     # As the original string will be cut during processing, if more than one match is found, the new index 
                      # was being printed. This manages the old index of the string.
        count = 0

        string = string if caseSen else string.lower()
        substring = substring if caseSen else substring.lower()

        gn.info("find", "Match(es) found at position(s): ", end='')
        while True:
            # Check if substring was found
            if (temp:=string.find(substring)) != -1:
                old    += temp+1
                gn.customPrint(f"{', ' if bool(count) else ''}{'**' if count%2 else '!!'}{old}##", end='')
                string  = string[temp+1:] # Cut original string
                count  += 1
            else:
                gn.customPrint('' if count > 0 else '-')
                gn.customPrint(f"Total: {'??' if not count else '!!'}{count}## match{'' if count == 1 else 'es'} found")
                break
        
        return 0
    
    # Never observed
    except Exception as e:
        return gn.unknownErr("find", e)
