# 
# Second 5.0 source code
# 
# Filename          : interpreter.py
# Brief description : Contains built-in commands and the base of the interpreter, the 
#                     Interpreter class, inherited from the Cmd class of the cmd module
#                     of the standard library of Python 3.12.4.
# 
# This software is a product of Infinite, Inc., and was written by
# CPythonist (http://cpythonist.github.io/) of the development team of Infinite, Inc.
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
# Please report any bugs and problems with the log files in the logs directory located 
# in the Second directory to the email address in http://cpythonist.github.io/contact.html.
# 
# TODO:
# 1. Find command - file and directory search.
# 

# Import error procedure
def importErr(module, error):
    # For logging
    import datetime
    import os
    print(f"SECOND5: Error: File import was unsuccessful. Second-5.0 was unable to start. Try reinstalling the program.\nMODULE : {module}")
    
    os.makedirs("logs", exist_ok=True)
    # Log the error
    with open(f"logs{os.sep}{module}Err.log", 'a', buffering=1) as f:
        f.write(f"\n\n{datetime.datetime.now()}\n{module}: importErr: {error.__class__.__name__}: {str(error)}\n{(15 + len(module) + len(error.__class__.__name__)) * '-'}\n")
    
    # Exit the program. sys.exit(1) is not used as I wanted to minimise the number of imported modules, as the 
    # error itself is due to a missing module.
    raise SystemExit(1)

# Imports
try:
    from bin import *
    import cmd
    import msvcrt
    import os
    import pathlib
    import re
    import shutil
    import subprocess
    import globalFile   as gn
    import intCommons   as comm
    import printStrings as ps

except (ImportError, FileNotFoundError, ModuleNotFoundError) as e:
    importErr("interpreter", e)

# Initialisation for use of ANSI escape codes
os.system('')


# Main class of the program
class Interpreter(cmd.Cmd):
    """
    Return codes each command of the interpreter:
    -3 - Fatal error: cannot be set :) (as interpreter will exit on encountering a fatal error, hence the name)
    -2 - Critical error: not sure if it can be seen using '!error'; can be seen using '$error' from symbol table
    -1 - Unknown error
     0 - Success
     1 - Error
     2 - User aborted
     3 - Error was reported, but some part worked as intended
     4 - Unknown command
     5 - Interpreter start
    """
    def __init__(self):
        super().__init__()
        self.accessPath = os.getcwd()
        os.chdir(os.path.expanduser('~'))

        if not gn.ANSI:
            # This regex was not written by me! This removes all ANSI escape codes if the terminal does not support them.
            self.ANSIRemoved = re.compile(br'(?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])')
            gn.PROMPT        = (self.ANSIRemoved.sub(b'', gn.PROMPT.encode("utf-8"))).decode("utf-8")
        
        self.realPrompt = gn.PROMPT
        self.oldCDPath  = os.path.expanduser('~')
        self.title      = "Second 5"
        self.err        = 5

        try:
            printed = False
            if os.path.isdir(f"{self.accessPath}{os.sep}plugins"):
                for file in os.scandir(f"{self.accessPath}{os.sep}plugins"):
                    gn.customPrint("Info: Loading plugins...") if not printed else None
                    printed = True

                    if not os.path.isfile(file):
                        gn.error("interpreter: plugin", f"Is not a file: \"{file}\"")
                        continue
                    with open(file, 'r', buffering=1) as f:
                        for line in f:
                            self.onecmd(line)
        
        except FileNotFoundError:
            pass
    
    def default(self, line):
        """
        Override default method for parsing terminal and invalid commands.
        """
        line = [i for i in line.split() if not (i == '' or i.isspace())]
        print(f"Unknown command: \'{gn.RED if gn.ANSI else ''}{line[0]}{gn.RESET if gn.ANSI else ''}\'")
        return 4
    
    def emptyline(self):
        """
        Override default method for emptyline for passing without any error message.
        """
        return self.err

    def onecmd(self, line):
        """
        Taken from cmd.py module of standard library of CPython 3.12.4.
        Edited to add functionality of uppercase and mixed case commands, 
        accessing file commands and aliased commands.
        """
        if line.endswith('\\'):
            running = True
            while running:
                try:
                    continuation = input("... ")
                except EOFError:
                    gn.symTable["error"] = str(result:=self.err)
                    return result
                
                if not continuation.endswith('\\'):
                    running = False
                line = line[:-1] + continuation
        
        if line.strip() == "!error":
            print(self.err)
            gn.symTable["error"] = str(result:=self.err)
            return result
        
        cmd, arg, line = self.parseline(line)

        if not line:
            gn.symTable["error"] = str(result:=self.emptyline())
            return result
        if cmd is None:
            gn.symTable["error"] = str(result:=self.default(line))
            return result
        
        self.lastcmd = line

        if line == 'EOF' :
            self.lastcmd = ''
        if cmd == '':
            gn.symTable["error"] = str(result:=self.default(line))
            return result
        else:            
            try:
                func = getattr(self, "do_" + cmd.lower())
                gn.symTable["error"] = str(result:=func(arg))
                return result
            
            except AttributeError:
                try:
                    func = getattr(globals()['s' + cmd.lower()], cmd.upper())
                    gn.symTable["error"] = str(result:=func(self, arg))
                    return result
                
                except (KeyError, AttributeError):
                    if cmd.lower() == os.getlogin().lower():
                        gn.customPrint(":)")
                    else:
                        with open(f"{self.accessPath}{os.sep}saliases.txt", 'r', buffering=1) as f:
                            for l in f:
                                for i, char in enumerate(l):
                                    if char == '=':
                                        break
                                if cmd.lower() == l[:i].lower():
                                    gn.symTable["error"] = str(result:=self.onecmd(f"{l[i+1:]} {arg if arg is not None else ''}"))
                                    return result
                            else:
                                if not re.match(r"^[\d+\-*/().^ ]+$", line.replace('^', "**")):
                                    gn.symTable["error"] = str(result:=self.default(line))
                                    return result
                                
                                line = line.replace('^', "**")
                                try:
                                    print(eval(line, {"__builtins__": None}, {}))
                                    return 0
                                except Exception as e:
                                    print("unknownErr: Please report to developers")
                                    return -1

    def preloop(self):
        """
        Override default method for preloop for dynamic prompt and to remove ANSI escape codes if the terminal
        does not support them.
        """
        if not gn.ANSI:
            self.realPrompt = (self.ANSIRemoved.sub(b'', self.realPrompt.encode("utf-8"))).decode("utf-8")
        self.prompt = gn.promptUpdater(str(pathlib.Path(os.getcwd()).resolve()), self.realPrompt)

    def postcmd(self, stop, line):
        """
        Override to update dynamic prompt at the end of each loop.
        """
        if not gn.ANSI:
            self.realPrompt = (self.ANSIRemoved.sub(b'', self.realPrompt.encode("utf-8"))).decode("utf-8")
        self.prompt = gn.promptUpdater(str(pathlib.Path(os.getcwd()).resolve()), self.realPrompt)
        self.err = super().postcmd(stop, line)
        return self.err
    
    def do_bm(self, args):
        "Bookmarks a directory."
        return self.do_bookmark(args, calledFrom="bm")
    
    def do_bookmark(self, args, calledFrom="bookmark"):
        "Bookmarks a directory."
        try:
            args, opts = comm.parse(args)
            if len(args) != 1:
                return gn.error(calledFrom, "Incorrect format")
            if opts:
                return gn.error(calledFrom, f"Unknown option(s): {str(opts)[1:-1]}")
            
            if os.path.isdir(args[0]):
                gn.symTable["bm"]       = str(pathlib.Path(args[0]).resolve())
                gn.symTable["bookmark"] = str(pathlib.Path(args[0]).resolve())
            else:
                return gn.error(calledFrom, f"No such directory: \"{args[0]}\"")
            
            return 0
        
        except Exception as e:
            return gn.unknownErr(calledFrom, e)
    
    def do_clear(self, args):
        "Clears the output screen."
        return self.do_cls(args)

    def do_cls(self, args):
        "Clears the output screen."
        try:
            os.system("cls")
            print()
            return 0
        except Exception as e:
            return gn.unknownErr("cls", e)
    
    def do_copyright(self, args):
        "Displays the copyright information of Second."
        try:
            gn.customPrint(ps.copyright)
            return 0
        except Exception as e:
            return gn.unknownErr("copyright", e)
    
    def do_credits(self, args):
        "Displays credits."
        try:
            gn.customPrint(ps.credits)
            return 0
        except Exception as e:
            return gn.unknownErr("credits", e)
    
    def do_eof(self, args):
        "Exits the program."
        try:
            return gn.exit()
        except Exception as e:
            return gn.unknownErr("eof", e)
    
    def do_exit(self, args):
        "Exits the program."
        try:
            return gn.exit()
        except Exception as e:
            return gn.unknownErr("exit", e)
    
    def do_get(self, args):
        "Gets an interpreter variable's value."
        try:
            args, opts = comm.parse(args)

            if not args:
                toBeSearched = ''
            else:
                toBeSearched = args
            if opts:
                return gn.error("get", f"Unknown option(s): {str(opts)[1:-1]}")
            
            # Loop through the symbol table and print accordingly
            found = False
            for i in gn.symTable:
                if not toBeSearched:
                    print(f"\'{i}\' = \"{gn.symTable[i]}\"")
                    continue
                for j in toBeSearched:
                    if j.lower() == i.lower():
                        print(f"\"{gn.symTable[i]}\"")
                        found = True
                if found:
                    break
            else:
                if toBeSearched:
                    return gn.error("get", f"No such variable(s): \'{str(args)[1:-1]}\'")

            return 0
            
        except Exception as e:
            return gn.unknownErr("get", e)
    
    def do_help(self, args, calledFrom="help"):
        "Displays the help menu."
        try:
            args, opts = comm.parse(args)

            # General help
            if len(args) == 0 and not opts:
                # Built-in commands are commands (i.e. functions) defined in this class in the format "do_<command-name>()"
                # External commands are commands (i.e. modules) defined in the "bin" directory of the format "s<command-name>.py[d]", 
                # containing a function of the format <command-name-uppercase>()
                builtIncommands  = [i for i in dir(self) if i.startswith("do_")]
                externalCommands = [globals()[module] for module in globals() if module.startswith('s') and hasattr(globals()[module], module[1:].upper())]

                # Find the longest command name
                maxLen = 0
                for i in builtIncommands:
                    if len(i) > maxLen:
                        maxLen = len(i)
                for i in externalCommands:
                    if len(i.__name__) > maxLen:
                        maxLen = len(i.__name__)

                # For built-in commands, file core\printStrings.py has the help strings, defined in a class "HelpStrs", 
                # with the variable name "<command-name>Help"
                if builtIncommands:
                    gn.customPrint("&&**BUILT-IN COMMANDS:##")
                for i in builtIncommands:
                    print(f"{i[3:].upper():<{maxLen}}{comm.tillChar(getattr(ps.HelpStrs, i[3:] + "Help")[1:])}")
                
                # For external commands, the help strings are in the format <command-name-module>.helpStr
                if externalCommands:
                    gn.customPrint("\n&&**EXTERNAL COMMANDS:##")
                for i in externalCommands:
                    try:
                        print(f"{i.__name__[5:].upper():<{maxLen}}{comm.tillChar(getattr(i, "helpStr")[1:])}")
                    except AttributeError:
                        print(f"{i.__name__[5:].upper():<{maxLen}}-")
            
            # Specific command help
            elif len(args) == 1 and not opts:
                try:
                    # Attempt to read help string variable in built-in commands
                    temp = getattr(ps.HelpStrs, args[0].lower() + "Help")
                    gn.info(calledFrom, temp.removeprefix('\n'), end='')
                    return 0
                except AttributeError:
                    try:
                        temp = getattr(globals()['s' + args[0].lower()], "helpStr")
                        gn.info(calledFrom, temp.removeprefix('\n'), end='')
                        return 0
                    except AttributeError:
                        return gn.error(calledFrom, f"No help string: \'{args[0]}\'")
                    except KeyError:
                        gn.error(calledFrom, f"No such command: \'{args[0]}\'")
                        return 1
            else:
                return gn.error(calledFrom, f"Incorrect format")
            return 0
        
        except Exception as e:
            return gn.unknownErr(calledFrom, e)
    
    def do_history(self, args):
        "Displays the history of the program."
        try:
            gn.customPrint(ps.history)
            return 0
        except Exception as e:
            return gn.unknownErr("history", e)
    
    def do_man(self, args):
        "Print manual pages (help pages) for commands."
        try:
            args, opts = comm.parse(args)
            if len(args) == 1:
                if not opts:
                    self.do_help(args[0], calledFrom="man")
                else:
                    return gn.error("man", f"Unknown option(s): {str(opts)[1:-1]}")
            else:
                return gn.error("man", f"Incorrect format")
        except Exception as e:
            return gn.unknownErr("man", e)
    
    def do_plugin(self, args):
        "Create a plugin (startup) script."
        try:
            args, opts = comm.parse(args)
            err = 0

            if not args:
                return gn.error("plugin", "No plugin specified")
            
            if opts:
                if len(opts) == 1:
                    # 'r' option is for removing a plugin
                    if opts[0] != 'r':
                        return gn.error("plugin", f"Unknown option: \'{opts[0]}\'")
                    
                    # If plugin directory exists
                    if os.path.isdir(f"{self.accessPath}{os.sep}plugins"):
                        err = 0
                        # Iterate through the arguments and the plugins directory and remove file if present.
                        # found variable is for printing error message
                        for arg in args:
                            found = False
                            for file in os.scandir(f"{self.accessPath}{os.sep}plugins"):
                                if arg.lower() == file.name.lower():
                                    os.remove(file)
                                    found = True
                            if not found:
                                err = gn.error("plugin", f"No such plugin: \"{arg}\"")
                        return err
                    
                    else:
                        return gn.error("plugin", "No plugins found")
            
            # If plugin directory does not exist.
            # These are executed if there are no options specified (i.e. the user wants to add plugins)
            
            os.makedirs(f"{self.accessPath}{os.sep}plugins", exist_ok=True)
            
            # Iterate through the arguments and copy the file to the plugins directory, if it exists
            for file in args:
                if os.path.isfile(file):
                    if not os.path.isfile(f"{self.accessPath}{os.sep}plugins{os.sep}{file.split(os.sep)[-1]}"):
                        shutil.copy(file, f"{self.accessPath}{os.sep}plugins{os.sep}{file}")
                        continue
                    
                    try:
                        choice = input("Destination file already exists. Overwrite ([y]/n)? ").lower()
                    except EOFError:
                        err = gn.error("plugin", "Invalid option. No changes were made")  # These two are needed as even though else block is present because 
                        continue                                                          # if EOFError is raised, variable choice will not be defined.
                    
                    if choice in ('', 'y', 'yes') or choice.isspace():
                        shutil.copyfile(file, f"plugins{os.sep}{file}")
                    elif choice in ('n', 'no'):
                        continue
                    else:
                        err = gn.error("plugin", "Invalid option. No changes were made")
                
                else:
                    err = gn.error("plugin", f"No such file: \"{file}\"")
            
            return err
        
        except Exception as e:
            return gn.unknownErr("plugin", e)

    def do_quit(self, args):
        "Quits the program."
        try:
            return gn.exit()
        except Exception as e:
            return gn.unknownErr("quit", e)
    
    def do_second(self, args):
        "Displays the developer and operating system information of Second 5."
        try:
            args, opts = comm.parse(args)

            if not args:    
                if not opts:
                    gn.customPrint(ps.secondFormatted)
                    return 0
                elif len(opts) == 1:
                    # 'c' option is for copying output to clipboard
                    if opts[0] == 'c':
                        gn.customPrint(ps.secondFormatted)
                        code = subprocess.run(["clip.exe"], input=ps.secondUnformatted.encode('utf-8'), check=True)
                        # code will be int
                        return int(bool(code))
                    else:
                        return gn.error("second", f"Unknown option: {str(opts)[1:-1]}")
                elif len(opts) > 1:
                    return gn.error("second", f"Unknown options: {str(opts)[1:-1]}")
            
            # User entered '6' :)
            elif len(args) == 1 and not opts:
                if (args[0].replace('.', '', 1).isnumeric()) and (float(args[0]) == int(str(gn.__version__).split('.')[0]) + 1):
                        gn.customPrint("&&SECOND6:## !!You got to wait!## Check for updates at __http://cpythonist.github.io/second.html## or __http://github.com/cpythonist##!")
                        return 0
                else:
                    return gn.error("second", f"Unknown argument(s): {str(args)[1:-1]}")
            
            else:
                return gn.error("second", f"Unknown argument(s): {str(args)[1:-1]}")
        
        # Never observed
        except Exception as e:
            return gn.unknownErr("second", e)
    
    def do_set(self, args):
        "Sets interpreter variables."
        try:
            args, opts = comm.parse(args)
            # Check for incorrect format
            if opts:
                return gn.error("set", f"Unknown option(s): {str(opts)[1:-1]}")
            
            if len(args) == 2:
                # Check if user is trying to modify variables bookmark, bm or error manually
                if args[0].lower() in ("bm", "bookmark"):
                    return gn.error("set", "Action not allowed; Use bm or bookmark command")
                elif args[0].lower() == "error":
                    return gn.error("set", "Action not allowed; Variable error cannot be changed manually")
                gn.symTable[args[0]] = args[1]
            elif not args:
                for var in gn.symTable:
                    gn.customPrint(f"\'{var}\' = \"{gn.symTable[var]}\"")
            else:
                return gn.error("set", "Incorrect format")
            
            return 0

        except Exception as e:
            return gn.unknownErr("set", e)
    
    def do_stop(self, args):
        "Pauses the program and waits for user to press any key."
        try:
            gn.customPrint("Press any key...")
            msvcrt.getch()
            return 0
        except Exception as e:
            return gn.unknownErr("stop", e)
    
    def do_ver(self, args):
        "Displays the version of Second interpreter."
        return self.do_version(args, calledFrom="ver")
    
    def do_version(self, args, calledFrom="version"):
        "Displays the version of Second interpreter."
        try:
            gn.customPrint(str(gn.__version__))
            return 0
        except Exception as e:
            return gn.unknownErr(calledFrom, e)
    
    def do_where(self, args):
        "Displays the location of a command."
        try:
            args, opts = comm.parse(args)
            if not args:
                return gn.error("where", "Incorrect format.")
            
            if opts:
                return gn.error("where", f"Unknown option(s): {str(opts)[1:-1]}")
            
            # This variable checks if only a single argument was passed (as the program needs to print the argument 
            # if multiple arguments were passed)
            singleComm = True if len(args) == 1 else False
            
            for arg in args:
                # Check if the argument is a built-in: First preference is given to built-in commands. They cannot
                # be overwritten.
                if getattr(self, "do_" + arg.lower(), None) != None:
                    print(f"{(arg.upper() + ': ') if not singleComm else ''}Built-in command")
                
                # Check if argument is "wife" :)
                elif arg.lower() == "wife":
                    print(f"{arg.upper()}: 404-Not found")
                
                else:
                    # Check if command is located in the directory bin. Second command files are in the format
                    # s<command-name>.py[d]
                    # These can be overwridden by the user, either by deleting the actual file, or by adding a 
                    # .py file with the same base name.
                    for file in os.scandir(os.path.join(self.accessPath, "bin")):
                        if os.path.isfile(file) and ((temp:=file.name.endswith(".pyd")) or file.name.endswith(".py")) and (file.name != "__init__.py" or file.name != "__init__.pyd"):
                            if file.name.lower() == ('s' + arg.lower() + (".pyd" if temp else ".py")):
                                print(f"{(arg.upper() + ': ') if not singleComm else ''}{file.path}")
                                break
                    else:
                        return gn.error("where", f"No such file or built-in: \"{arg}\"")
                
            return 0
        
        except FileNotFoundError:
            return gn.error("where", "Directory \"bin\" was not found.")
        
        except Exception as e:
            return gn.unknownErr("where", e)
