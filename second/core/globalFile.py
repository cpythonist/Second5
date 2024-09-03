# 
# Second 5.0 source code
# 
# Filename          : globalFile.py
# Brief description : Contains globally used functions of the program to be accessible 
#                     to the whole program.
# 
# This software is a product of Infinite, Inc., and was written by
# CPythonist (http://cpythonist.github.io) of the development team of Infinite, Inc.
# 
# 
# Copyright 2024 Infinite Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 
# 
# Please refer to http://cpythonist.github.io/second/documentation/secondDoc5.0.html
# for documentation.
# Please report any bugs to the email address in http://cpythonist.github.io/contact.html.
# 

# Version declaration
__version__ = 5.0

# Import error procedure
def importErr(module, error):
    import datetime
    import os
    print(f"SECOND5: Error: File import was unsuccessful. Second-5.0 was unable to start. Try reinstalling the program.\nMODULE : {module}")
    
    os.makedirs(os.path.join("logs"), exist_ok=True)
    with open(f"logs{os.sep}{module}Err.log", 'a', buffering=1) as f:
        f.write(f"\n\n{datetime.datetime.now()}\n{module}: importErr: {error.__class__.__name__}: {str(error)}\n{(15 + len(module) + len(error.__class__.__name__)) * '-'}\n")
    
    raise SystemExit(1)

# Imports
try:
    import ctypes
    import datetime
    import getpass
    import itertools
    import msvcrt
    import os
    import pickle
    import platform
    import re
    import sys
    import time
    import traceback

except (ImportError, ModuleNotFoundError, FileNotFoundError) as e:    
    importErr("globalFile", e)

# Program path
progPath      = os.getcwd()
# Declaration of escape codes for text-formatting
BOLD          = "\033[1m"
BLINK         = "\033[5m"
BLUE          = "\033[94m"
CLS           = "\033[H\033[J"
CYAN          = "\033[96m"
GREEN         = "\033[92m"
HEADER        = "\033[95m"
RED           = "\033[91m"
RESET         = "\033[0m"
UNDERLINE     = "\033[4m"
YELLOW        = "\033[93m"
# Interpreter symbol table
symTable      = {
    "home": os.path.expanduser("~"),
    "bookmark": os.path.expanduser("~"),
    "error": 5
}
# Default prompt variable
defaultPrompt = f"{BLUE}%U{RESET}->{BLUE}%S%R{RESET}&&{GREEN}%P{RESET}(S5):\n{GREEN}${RESET} "


def isANSISupported():
    """
    Checks if the terminal supports ANSI sequences.
    If yes, return True, else False.
    Thanks to Stack Overflow for this code snippet!
    """
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    while msvcrt.kbhit():
        msvcrt.getch()
    # Try writing a sample escape sequence and use '\b' to erase it
    sys.stdout.write("\x1b[6n\b\b\b\b")
    sys.stdout.flush()
    sys.stdin.flush()
    if msvcrt.kbhit():
        if ord(msvcrt.getch()) == 27 and msvcrt.kbhit():
            if msvcrt.getch() == b"[":
                while msvcrt.kbhit():
                    msvcrt.getch()
                return sys.stdout.isatty()
    return False


def customPrint(*string:str, end:str='\n', sep:str=' ', flush:bool=False, returnValue:bool=False) -> None | str:
    """
    Custom function for output to sys.stdout with easier text-formatting.
    Uses regular expressions to evaluate strings given and replace characters
    as necessary with formatting data.
    Formatting options:
        ?? -> Red
        ?! -> Yellow
        !! -> Green
        ** -> Cyan
        ^^ -> Blue
        && -> Bold
        __ -> Underline
        ## -> Reset
    Returns None if returnValue is False else returns edited string.
    """
    finalStr:list = []
    
    for i in string:
        for pattern, repl in replace:    
            i = re.sub(pattern, repl, i)
        finalStr.append(i)
    
    if not returnValue:
        sys.stdout.write(sep.join(finalStr) + end)
        sys.stdout.flush() if flush else None
        return None
    else:
        return (sep.join(finalStr) + end)


def readSettings(path) -> None:
    """
    Function to read settings from the file ssettings.dat.
    If the file is found and data is valid, settings are loaded into global variable(s) for later use.
    Else if the file is:
        1. Empty: Attempts to write default value(s) into file.
        2. Invalid: Attempts to erase the file and write default value(s) into the file.
        3. Not found: Attempts to create the file and write default value(s) into the file.
    Returns None.
    """
    global PROMPT           # Global prompt variable
    isDataLoaded = False    # For checking if settings has been read in one of the conditions

    def writeDefaultSettings() -> None:
        """
        Function to write default settings into file 'ssettings.dat'.
        Returns None.
        """
        try:
            with open(f"{path}{os.sep}ssettings.dat", 'wb') as f:
                pickle.dump({"prompt": defaultPrompt}, f)
        except PermissionError:    # Access is denied
            error("startup5", "Access is denied to write to file: \'ssettings.dat\'")

    try:
        with open(f"{path}{os.sep}ssettings.dat", 'rb+') as f:
            data         = pickle.load(f)    # Data is stored in dictionary
            isDataLoaded = True
            PROMPT       = data["prompt"]
    
    except EOFError:
        # Check if the data was loaded (for checking empty ssettings.dat file)
        if not isDataLoaded:
            # Try to correct file ssettings.dat
            info("startup5", "\'ssettings.dat\': File is empty. Writing default values...", printFunc=True)
            writeDefaultSettings()
            PROMPT = defaultPrompt
    
    except FileNotFoundError:    # File ssettings.dat not found
        info("startup5", "\'ssettings.dat\': Not found. Writing default values...", printFunc=True)
        writeDefaultSettings()
        PROMPT = defaultPrompt
    
    except (pickle.UnpicklingError, KeyError):    # Invalid data
        info("startup5", f"\'ssettings.dat\': Invalid data. Write default values [y]/n ?\n{YELLOW if ANSI else ''}${RESET if ANSI else ''} ", printFunc=True, end='')
        try:
            choice = input().lower()
            if choice in ('', 'y', 'yes') or choice.isspace():
                writeDefaultSettings()
                PROMPT = defaultPrompt
            elif choice in ('n', 'no'):
                info("startup5", "Loading with default settings...", printFunc=True)
                PROMPT = defaultPrompt
            else:
                error("startup5", "Invalid option. Loading with default settings...")
                PROMPT = defaultPrompt
        except EOFError:
            PROMPT = defaultPrompt
    
    except Exception as e:    # Never observed till now
        unknownErr("startup5", e)


def promptUpdater(path:str, prompt:str):
    """
    Function to update the dynamic prompt of Second. Returns updated prompt.
    Valid characters following '%' to be a placeholder
        %(N|n) -> Newline
        %(P|p) -> Path (current working directory)
        %(R|r) -> Release number
        %(S|s) -> OS name
        %(U|u) -> Username
        %(%)   -> % character
    Has weird behaviour with some prompts in some specific formats, was unable to be fixed.
    """
    while '%' in prompt.upper():
        for i in range(prompt.index('%'), len(prompt)):
            if prompt[i] == '%':
                if prompt[i+1] in "Uu":
                    prompt = prompt[:i] + getpass.getuser() + prompt[i+2:]
                
                elif prompt[i+1] in "Ss":
                    prompt = prompt[:i] + platform.system() + prompt[i+2:]
                
                elif prompt[i+1] in "Rr":
                    ver = platform.version(); rel = platform.release()

                    if rel == "10":
                        rel = "11" if (int(ver.split('.')[2]) > 22000) else "10"
                    
                    prompt = prompt[:i] + rel + prompt[i+2:]
                
                elif prompt[i+1] in "Pp":
                    prompt = prompt[:i] + path + prompt[i+2:]
                
                elif prompt[i+1] in "Nn":
                    prompt = prompt[:i] + '\n' + prompt[i+2:]
                
                elif prompt[i+1] == '%':
                    prompt = prompt[:i+1] + prompt[i+2:]
                
                break
    
    return prompt

# Check if terminal supports ANSI
ANSI    = isANSISupported()
# For customPrint function for replacing formatters with ANSI codes
replace = (
    (r"\?\?", (RED if ANSI else '')),
    (r"\?!", (YELLOW if ANSI else '')),
    (r"!!", (GREEN if ANSI else '')),
    (r"\*\*", (CYAN if ANSI else '')),
    (r"\^\^", (BLUE if ANSI else '')),
    (r"\&\&", (BOLD if ANSI else '')),
    (r"__", (UNDERLINE if ANSI else '')),
    (r"\#\#", (RESET if ANSI else '')),
)

def info(func:str, string:str, custom=False, info=False, printFunc=False, end='\n'):
    """
    Print information to stdout and return None.
    """
    if not custom and not info:
        print(f"{func + ': ' if printFunc else ''}{string}", end=end)
    elif not custom and info:
        print(f"{BOLD if ANSI else ''}{func.upper()}:{RESET if ANSI else ''} {CYAN if ANSI else ''}Info:{RESET if ANSI else ''} {func + ': ' if printFunc else ''}{string}", end=end)
    elif custom and info:
        customPrint(f"&&{func.upper()}:## **Info:## {func + ': ' if printFunc else ''}{string}", end=end)
    else:
        customPrint(f"{func + ': ' if printFunc else ''}{string}", end=end)

def error(func:str, string:str, custom=False, info=False, end:str='\n'):
    """
    Print errors to stdout and return error code 1.
    """
    if not custom and not info:
        print(func.lower() + ":", string, end=end)
    elif not custom and info:
        print(f"{func.lower()}: {BOLD if ANSI else ''}{func.upper()}:{RESET if ANSI else ''} {RED if ANSI else ''}Error:{RESET if ANSI else ''} {string}", end=end)
    elif custom and info:
        customPrint(f"{func.lower()}: &&{func.upper()}:## ??Error:## {string}", end=end)
    else:
        customPrint(f"{func.lower()}: {string}", end=end)
    return 1

def unknownErr(func:str, err:Exception, end='\n'):
    """
    Print unknown errors to stdout and return unknown error code -1.
    """
    os.makedirs(f"{progPath}{os.sep}logs", exist_ok=True)
    with open(f"{progPath}{os.sep}logs{os.sep}commErr.log", 'a', buffering=1) as f:
        f.write(f"""
{datetime.datetime.now()}
{func.upper()}: Unknown Error:
{(temp:=traceback.format_exc())}
{len(temp.split('\n')[-1]) * '-'}\n
""")
    print(f"{BOLD if ANSI else ''}{func.upper()}:{RESET if ANSI else ''} {RED if ANSI else ''}unknownErr:{RESET if ANSI else ''} {err.__class__.__name__}: {err}", end=end)
    return -1

def exit():
    print(f"{BOLD if ANSI else ''}SECOND5:{RESET if ANSI else ''} Exit!")
    sys.exit(0)


# Loading animation
class Loading:
    """
    Just a loading animation class, used for KILL and SYSINFO during testing, due to 
    psutil's task search and systeminfo command taking too much time, then removed as 
    performance was improved significantly after psutil was removed and another solution 
    was implemented.
    """
    def __init__(self):
        # self.done will be changed by external means
        self.done = False
    
    def loadingAnimation(self):
        self.done = False
        for i in itertools.cycle(['-', '\\', '|', '/']):
            if self.done:
                break
            sys.stdout.write(i + '\r')
            sys.stdout.flush()
            time.sleep(0.1)
