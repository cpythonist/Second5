import os

os.chdir("..{os.sep}bin")
for file in os.scandir('.'):
    if file.name != "__init__.py":
        os.system(f"python -m --module {file.name}")

os.chdir("..\\core")
for file in os.scandir('.'):
    os.system(f"python -m nuitka --module {file.name}")
