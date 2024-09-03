# 
# Second 5 standard library command
# Copyright (c) 2024, Infinite Inc.
# Written by Thiruvalluvan Kamaraj
# Licensed under the Apache-2.0 License.
# 

import re
import subprocess as sp
import globalFile as gn
import intCommons as comm

helpStr = """
Lists processes, or searches for processes.
Syntax:
    LIST [process1 process2 ...] [-n] [-p] [-m]
Arguments:
    process<num> -> The name of the processes to search for
Options:
    -n           -> Print process names
    -p           -> Print process IDs
    -m           -> Print process memories
"""

def LIST(interpreter, args):
    "Lists processes, or searches for processes."
    # Okay, seriously, this needs extensive documentation.
    # The process search feature surely needs some more effort (like not printing the column titles
    # when the process could not be found, printing the title columns again if one of the process names
    # could not be found and an error message is displayed in the middle, etc.), but I don't want to do 
    # that :( (now). I simply can't.
    try:
        args, opts = comm.parse(args)
        printProcessNames, printProcessIDs, printProcessMemories = False, False, False
        processesToMatch = None     # TODO: Kept for extending the list command to searching for a particular task

        # Parse options
        if opts:
            opts.sort()
            if not (set(opts) <= {'m', 'n', 'p'}):
                return gn.error("list", f"Unknown option(s): {str(opts)[1:-1]}")
            if 'n' in opts:
                printProcessNames    = True
            if 'p' in opts:
                printProcessIDs      = True
            if 'm' in opts:
                printProcessMemories = True
        else:
            printProcessNames, printProcessIDs, printProcessMemories = True, True, True

        output = sp.run(["tasklist"], capture_output=True)              # Run tasklist command, capturing output
        tasklist = output.stdout.decode("utf-8").split('\n')            # Tasklist command output, decode and split on newlines
        regex   = r"^(.+?)\s+(\d+)\s(.+)\s+(\d+)\s+(\d*,*\d+\sK).*$"    # Regex for matching output of tasklist command
        names      = []
        ids        = []
        memories   = []

        # Process tasklist command output
        for task in tasklist:
            matches = re.match(regex, task)
            if matches is not None:
                names.append(matches.group(1))
                ids.append(matches.group(2))
                memories.append(matches.group(5))
        
        # Remove commas from memory values
        for i, memory in enumerate(memories):
            result = ''
            for char in memory:
                if char != ',':
                    result += char
            memories.pop(i)
            memories.insert(i, result)
        
        # Calculate padding based on the longest value and add 3 for spacing.
        paddingNames = len(max(names + ["Process name"], key=len)) + 3
        paddingIDS = len(max(ids + ["Process ID"], key=len)) + 3
        paddingMemories = len(max(memories + ["Memory"], key=len)) + 3

        if not args:
            # Print the column titles (based on the variables declared using the options provided)
            if printProcessNames:
                gn.customPrint(f"{"Process name":<{paddingNames}}", end='')
            if printProcessIDs:
                gn.customPrint(f"{"Process ID":<{paddingIDS}}", end='')
            if printProcessMemories:
                gn.customPrint(f"{"Memory":<{paddingMemories}}", end='')
            print()
            
            # Print the values (based on variables defined from options provided)
            for i in range(len(names)):
                if printProcessNames:
                    gn.customPrint(f"{names[i]:<{paddingNames}}", end='')
                if printProcessIDs:
                    gn.customPrint(f"{ids[i]:<{paddingIDS}}", end='')
                if printProcessMemories:
                    # strip() function is used to remove the leading whitespaces (memory's alignment in 
                    # the tasklist command leads to whitespace in front) and trailing whitespace (if any)
                    gn.customPrint(f"{memories[i].strip():<{paddingMemories}}", end='')
                print()
            
            return 0
        
        else:
            # Print the column titles (based on the variables declared using the options provided)
            if printProcessNames:
                gn.customPrint(f"{"Process name":<{paddingNames}}", end='')
            if printProcessIDs:
                gn.customPrint(f"{"Process ID":<{paddingIDS}}", end='')
            if printProcessMemories:
                gn.customPrint(f"{"Memory":<{paddingMemories}}", end='')
            print()

            err = 0
            # Print the values (based on variables defined from options provided)
            for arg in args:
                found = False
                # Current argument (process name) is checked against each entry in list names
                for i, name in enumerate(names):
                    if arg.lower() != name.lower():
                        continue
                    if printProcessNames:
                        gn.customPrint(f"{name:<{paddingNames}}", end='')
                    if printProcessIDs:
                        gn.customPrint(f"{ids[i]:<{paddingIDS}}", end='')
                    if printProcessMemories:
                        gn.customPrint(f"{memories[i].strip():<{paddingMemories}}", end='')
                    found = True
                    print()
                # err will contain error code for last error encountered
                if not found:
                    err = gn.error("list", f"No such process: \"{arg}\"")
            
            return err

    except Exception as e:
        return gn.unknownErr("list", e)
