# The Second5 Interpreter
The fifth major version of the Second interpreter.<br>
Second is a family of command-line interpreters developed by Infinite, with the aim of becoming a cross-platform interpreter used widely across many devices. Second draws inspiration from cmd.exe (from Microsoft Windows) and GNU Bash, and aims to be as powerful as them.<br>
<br>
Second 5 can used after installing the pre-built binaries provided (## TODO: Provide the installer) or by [building it from source yourself](https://github.com/cpythonist/Second5/edit/main/README.md#building).<br>
<br>
<p align="center">
  <img width="100" height="100" src="https://github.com/cpythonist/assets/blob/main/second5/second5.ico">
</p>
<p align="center">
  <img src="https://github.com/cpythonist/assets/blob/main/second5/second5help.png">
</p>
<br>
Documentation of the interpreter can be found at [the Second 5 Docs](http://cpythonist.github.io/second/documentation/secondDoc5.0.html).<br>
To contact the developer (me), please see [my contact page](http://cpythonist.github.io/contact.html).
## Building
Please see the files `runRequirements.txt` and `compileRequirements.txt` in the main branch for the requirements needed for running the program and compiling the program, respectively.<br>
## History
### Second 0.1
Development started in late 2020. The first implementation of the interpreter could not be published as a result of the program crashing when the `time` command was executed. The first implementation, Second 0.1 (then called CLI, with only one file named `CLI.py`), had a live clock when the `time` command was entered. This could be stopped and normal control could be resumed by interrupting the clock (`^C`). But this, due to unknown reasons, crashed the program if the inputs were continuously interrupted using `^C` after resuming normal control of the shell.<br>
### Second 1
The "live clock" idea was then shelved and Second-1.0 was published in early 2021. It had extrememly basic parsing abilities, with it receiving a command name in one input prompt, then receiving the arguments individually in separate prompts, with no option support.<br>
Second-1.1 was released fixing some bugs in the software.<br>
### Second 2
Second-2.0 was released with the same parsing abilities, but new commands were added and colour support was implemented, even though this made it unusable on terminals which do not support ANSI escape codes as the interpreter did not check for ANSI support.<br>
### Second 3
Second-3.0 was released in 2023, with a more powerful parser, which allowed single-line commands to be given to it. But the Second 3 parser required that all arguments must be enclosed in single- or double-quotes, with only one type of quote allowed for each command. It worked by splitting the input across the quote characters and getting the parts as arguments. Second 3 also had a larger library of commands, with many new commands like `prompt`, `title` and `start`. Second 4 also offered some of the commands from Second 1 and 2 that were discontinued in Second 3.<br>
### Second 4
Second-4.0 was made in early 2024, with a similar parser, but with different implementation that slightly varied in usage from the Second 3 parser. It had a larger library of commands with new commands like `dir`, `kill` and `tree`.<br>
### Second 5
Second-5.0 was made in the fall of 2024. It had parsing capabilities on par of the interpreters of major operating systems, like `cmd.exe` and GNU Bash. It has a extremely large command library compared to Second 4, with many commands being added for various purposes and many commands have other names to help users from more popular interpreters adapt to the new environment (like for copying files or directories, the `copy` command is directly called by the `cp` with its own name). Second 5 also introduces aliasing commands, which is used to execute a command from a different name. It also provides an extensible command library, the first one to implement it in the Second interpreter family, with many of the default commands (excluding built-in commands) able to be replaced with the user's own custom commands. Second 5 also includes more reliable and consistent error reporting and logging.<br>
<br>
Source code of the Second 5 Interpreter.
