# Second 5.0 source code
#
# Filename: second5.py
# Brief description: Contains the program that accesses all the files and runs the program.
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
# Improvements in Second 5.0:
#   1. More powerful parser
#   2. Added support for multiple arguments to commands
#   3. Added new commands (DISPLAY, FIND, FONT, SYSINFO, CLEAR, LS, MAKE, RUN, etc.)
#   4. Improved existing commands (like TREE, DIR, etc.)
# 
# Unrealised (maybe added in later versions):
#   1. To add the Infinite 2D game engine.
#   2. To add the Viper compiler and interpreter.
#
# Please refer http://cpythonist.github.io/second/documentation/secondDoc5.0.html/
# for documentation.
# Please report any bugs to the email address in http://cpythonist.github.io/contact.html/.
# 

__version__ = 5.0
def importErr(module, error):
    import datetime
    import os
    print(f"SECOND5: Error: File import was unsuccessful. Second-5.0 was unable to start. Try reinstalling the program.\nMODULE : {module}")
    
    os.makedirs("logs", exist_ok=True)
    with open(f"logs{os.sep}{module}Err.log", "a", buffering=1) as f:
        f.write(f"\n\n{datetime.datetime.now()}\n{module}: importErr: {error.__class__.__name__}: {str(error)}\n{(15 + len(module) + len(error.__class__.__name__)) * '-'}\n")
    
    raise SystemExit(1)

# Imports
try:
    import ctypes
    import logging
    import os
    import sys
    import threading
    import traceback
    sys.path.insert(1, "core")
    import globalFile   as gn
    import interpreter  as ip
    import printStrings as ps
    import updater      as upd

except (ImportError, FileNotFoundError, ModuleNotFoundError) as e:
    importErr("main", e)

def main():
    try:
        # Initialisation for use of escape codes
        os.system('')
        gn.readSettings(os.getcwd())
        ctypes.windll.kernel32.SetConsoleTitleW("Second 5")

        prog = ip.Interpreter()
        gn.customPrint(ps.startString)
        
        # Run the updater function in a separate thread. Given parameters are the process ID of self process to 
        # be passed to installer, if updates are available.
        update = threading.Thread(name="updater", target=upd.updater, args=[str(os.getpid())])
        update.start()

        def printAndLogUnknownErrs(typ, exceptionStr):
            gn.customPrint(f"{gn.BOLD if gn.ANSI else ''}SECOND5:{gn.RESET + gn.RED if gn.ANSI else ''} {typ.lower()}Error:{gn.RESET if gn.ANSI else ''} {e.__class__.__name__}: {e}")
            # Log unknown Exception
            os.chdir(prog.accessPath)
            os.makedirs("logs", mode=0o777, exist_ok=True)
            handler = logging.FileHandler(filename=f"logs{os.sep}mainErr.log", mode='a')
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(logging.Formatter("\n%(asctime)s\n%(levelname)s: %(name)s: %(message)s"))
            logger = logging.getLogger("main")
            logger.addHandler(handler)
            logger.critical(f"""
{typ if typ == "Critical" else typ.upper()} ERROR:
{exceptionStr}
{len(exceptionStr.split('\n')[-1]) * '-'}\n
""")
        
        # KeyboardInterrupts to be caught in cmd module was either not possible or was difficult to implement, 
        # or I just do not know how to implement :)
        while True:
            try:
                prog.cmdloop()
            except KeyboardInterrupt:
                print()
            except Exception:
                gn.symTable["error"] = -2
                printAndLogUnknownErrs("Critical", traceback.format_exc())
    except KeyboardInterrupt:
        print()
    except Exception as e:
        printAndLogUnknownErrs("Fatal", traceback.format_exc())
        sys.exit(1)    

if __name__ == "__main__":
    main()
