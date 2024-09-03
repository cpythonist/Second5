# 
# Second 5.0 source code
# 
# Filename          : intCommons.py
# Brief description : Contains commons functions for the interpreter.
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
# Please refer to http://cpythonist.github.io/second/documentation/secondDoc5.0.html to
# for documentation.
# Please report any bugs to the email address in http://cpythonist.github.io/contact.html.
# 

# Imports
import os

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
    import subprocess
    import globalFile as gn

except (ModuleNotFoundError, ImportError, FileNotFoundError) as e:
    importErr("intCommons", e)

# def runCommandInsideCommand(commandWithArgs):
#     import second5
#     second5.prog.onecmd(commandWithArgs)


class Parser:
    def __init__(self, src) -> None:
        self.src = src
        self.char = ''
        self.pos = -1

        self.__readChar()
    
    def __readChar(self) -> None:
        if self.pos < len(self.src) - 1:
            self.pos += 1
            self.char = self.src[self.pos]
        else:
            self.char = '\0'
    
    def __readUnquotedArg(self):
        startPos = self.pos
        self.__readChar()
        while not self.char.isspace():
            if self.char == '\0':
                return self.src[startPos:self.pos+1]
            self.__readChar()
        return self.src[startPos:self.pos]
    
    def __readQuotedArg(self, quote):
        startPos = self.pos
        self.__readChar()
        while self.char != quote:
            if self.char == '\0':
                return self.src[startPos+1:self.pos+1]
            self.__readChar()
        return self.src[startPos+1:self.pos]
    
    def __readOption(self):
        startPos = self.pos
        self.__readChar()
        while not self.char.isspace():
            if self.char == '\0':
                return self.src[startPos+1:self.pos+1]
            self.__readChar()
        return self.src[startPos+1:self.pos]

    def parse(self):
        args      = []
        opts      = []
        self.char = ''
        self.pos  = -1
        self.__readChar()
        
        while self.char != '\0':
            if (temp:=(self.char == '\'')) or self.char ==  '"':
                arg = self.__readQuotedArg('\'' if temp else '"')
                if arg.startswith('$'):
                    if arg[1:] in gn.symTable:
                        arg = str(gn.symTable[arg[1:]])
                elif arg.startswith('`') and arg.endswith('`'):
                    pass
                args.append(arg)
                self.__readChar() # self.char will be ' ' if there is a space character.
                                  # To avoid that, we read it again.
            
            elif self.char == '-':
                opt = self.__readOption()
                opts.append(opt)
            
            else:
                arg = self.__readUnquotedArg()
                if arg.startswith('$'):
                    if arg[1:] in gn.symTable:
                        arg = str(gn.symTable[arg[1:]])
                # elif arg.startswith('`') and arg.endswith('`'):
                args.append(arg)
            
            self.__readChar()
        
        return args, opts


parser = Parser('')

def parse(string):
    parser.src = string
    return parser.parse()

def tillChar(string, char='\n'):
    for i, character in enumerate(string):
        if character == char:
            return string[:i]

def isNumber(string, floatsAllowed=False):
    try:
        return bool(int(string) if not floatsAllowed else float(string))
    except ValueError:
        return False

def printSysinfo(copy:bool):
    output = subprocess.run(["systeminfo"], capture_output=True)
    system = output.stdout.decode("utf-8").split('\n')

    copyStr = []
    count = 0
    for i in system:
        if (
            i.lower().startswith("os name") or 
            i.lower().startswith("os version") or 
            i.lower().startswith("os manufacturer") or 
            i.lower().startswith("original install date") or 
            i.lower().startswith("system manufacturer") or 
            i.lower().startswith("system model") or 
            i.lower().startswith("system type") or 
            i.lower().startswith("processor(s)") or 
            i.lower().startswith("total physical memory") or 
            i.lower().startswith("available physical memory") or 
            i.lower().startswith("virtual memory: max size") or 
            i.lower().startswith("virtual memory: available") or 
            i.lower().startswith("virtual memory: in use")
        ):
            gn.customPrint(("**", '', "!!")[count%3] + i.removesuffix('\r') + "##")
            count += 1
            if copy: copyStr += [i.removesuffix('\r')]
    
    return copyStr
