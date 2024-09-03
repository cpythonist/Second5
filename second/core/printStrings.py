# 
# Second 5.0 source code
# 
# Filename          : printStrings.py
# Brief description : Contains a collection of large strings that are too bulky to put
#                     in the main program files.
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

def importErr(module, error):
    import datetime
    import os
    print(f"SECOND5: Error: File import was unsuccessful. Second-5.0 was unable to start. Try reinstalling the program.\nMODULE : {module}")
    
    os.makedirs("logs", exist_ok=True)
    with open(f"logs{os.sep}{module}Err.log", 'a', buffering=1) as f:
        f.write(f"\n\n{datetime.datetime.now()}\n{module}: importErr: {error.__class__.__name__}: {str(error)}\n{(15 + len(module) + len(error.__class__.__name__)) * '-'}\n")
    
    raise SystemExit(1)

# Imports
try:
    from globalFile import __version__

except (ImportError, FileNotFoundError, ModuleNotFoundError) as e:
    importErr("printStrings", e)


# General strings
startString = f"""
&&!!Infinite Second 5## (version {__version__})
Developer: CPythonist (Infinite Inc.) (http://cpythonist.github.io)
For credits and copyright, see **CREDITS## and **COPYRIGHT##.
Licensed under the Apache License, Version 2.0.
Type 'help' without quotes for the help menu."""

secondFormatted = """&&**Second 5 (version 5.0)##
Developer: CPythonist (Infinite Inc.) (__http://cpythonist.github.io##)
License: Apache-2.0 (__http://www.apache.org/licenses/LICENSE-2.0##)
Base language (CPython) version: &&!!3.12.4##
Compiler (Nuitka) version: &&!!2.4.8##
Operating system: &&**Windows##
Windows version: &&**10, 11##
To get the source code, visit __http://github.com/cpythonist/Second5##.
To get the documentation, visit __http://cpythonist.github.io/second/documentation/secondDoc5.0.html##."""

secondUnformatted = """Second 5 (version 5.0)
Developed by Infinite, Inc.
Developer: CPythonist (http://cpythonist.github.io)
License: Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
Base language (CPython) version: 3.12.4
Compiler (Nuitka) version: 2.4.8
Operating system: Windows
Windows version: 10, 11
To get the source code, visit http://github.com/cpythonist/Second5.
To get the documentation, visit http://cpythonist.github.io/second/documentation/secondDoc5.0.html."""

copyright = """Copyright (c) 2024 Infinite Inc.
Licensed under the Apache License, Version 2.0.
Written by CPythonist (http://cpythonist.github.io)
All rights reserved."""

credits = """Thanks to all the authors and contributors of the programs and libraries used in this program:
(Note: Make sure to view in a wide enough terminal window for best results)
CPython  3.11.9 (Core language) : ^^http://python.org##
Nuitka   2.4.8  (Compiler)      : ^^http://nuitka.net##
psutil   6.0.0                  : ^^http://github.com/giampaolo/psutil##
Requests 2.32.3                 : ^^http://github.com/psf/requests##"""

history = """Note: Character '$' indicates the end of a line.$
The Second interpreter was invented by CPythonist in late 2020.$
The first implementation of the interpreter was very basic, but could not be continued as after running the \
'time' command (which gives a live clock and interrupting it with Ctrl+C would stop the clock), the interpreter \
would crash if Ctrl+C was repeated pressed or other specific activities.$
The actual first version, Second-1.0, was first implemented in 2021. Second-1.0 had extremely basic parsing \
abilities, and could only input a command, then get the arguments in a separate input prompt, so it had multiple \
prompts for one command.$
Second-2.0 followed with the same parser with added features (new commands) to the interpreter.$
Second-3.0 was made in 2023 and had an upgraded CPython interpreter - version 3.9.6. Second 3 had enormously \
advanced parsing compared to the previous two versions. All arguments and options can be entered on the same line, \
but each argument and option was required to have quotes around them, and only one type of quote symbol can be used \
in a single command.$
Second-4.0 was made in 2024. Second 4 removed the need for quotes, but could only perform operations if the quotes, \
if used (in cases were quoted arguments are needed, for example, when a directory name has spaces) were of a single \
type.$
Second 5 was also made in 2024. It has major upgrades to parsing, able to parse on par with interpreters like \
cmd.exe and Bash and provides far more powerful and flexible commands such as allowing variable number of arguments \
to a command.$
For more information, please refer to http://cpythonist.github.io/second.html/."""


class HelpStrs:
    """
    Contains help strings for built-in commands.
    """

    bmHelp = """
Bookmarks a directory.
Syntax:
    BM directory
Argument:
    directory -> Directory to be bookmarked
"""

    
    bookmarkHelp = """
Bookmarks a directory.
Syntax:
    BOOKMARK directory
Argument:
    directory -> Directory to be bookmarked
"""

    clearHelp = """
Clears the output screen.
Syntax:
    CLEAR
"""

    clsHelp = """
Clears the output screen.
Syntax:
    CLS
"""

    copyrightHelp = """
Displays the copyright information of Second.
Syntax:
    COPYRIGHT
"""

    creditsHelp = """
Displays credits.
Syntax:
    CREDITS
"""

    eofHelp = """
Exits the program.
Syntax:
    ^Z (CTRL+Z)
"""

    exitHelp = """
Exits the program.
Syntax:
    EXIT
"""

    getHelp = """
Gets an interpreter variable's value.
Syntax:
    GET [variable]
Argument:
    variable -> Variable to be printed
"""

    helpHelp = """
Displays the help menu.
Syntax:
    HELP [command]
Argument:
    command -> Command to display help for
"""

    historyHelp = """
Displays the history of the program.
Syntax:
    HISTORY
"""

    manHelp = """
Print manual pages (help pages) for commands.
Syntax:
    MAN command
Argument:
    command -> Command to display man page for
"""

    pluginHelp = """
Create a plugin (startup) script.
Syntax:
    PLUGIN name script
Arguments:
    plugin -> Name of the plugin to be added
    script -> Second script for the plugin
Option:
    -r     -> Remove a plugin
"""

    quitHelp = """
Quits the program.
Syntax:
    QUIT
"""

    secondHelp = """
Displays the developer and operating system information of Second 5.
Syntax:
    SECOND [-c]
Option:
    -c -> Copies the command output to clipboard
"""

    setHelp = """
Sets interpreter variables.
Syntax:
    SET [variable value]
Arguments:
    variable -> Name of the variable
    value    -> Value of the variable
"""

    stopHelp = """
Pauses the program and waits for user to press any key.
Syntax:
    STOP
"""

    verHelp = """
Displays the version of Second interpreter.
Syntax:
    VER
"""

    versionHelp = """
Displays the version of Second interpreter.
Syntax:
    VERSION
"""

    whereHelp = """
Displays the location of a command.
Syntax:
    WHERE command
Argument:
    command -> Name of the command
"""
