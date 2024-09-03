import os
import shutil

os.chdir("bin")
os.makedirs("bin", exist_ok=True)
for fileOrDir in os.scandir('.'):
    if os.path.isdir(fileOrDir):
        shutil.rmtree(fileOrDir)
    elif os.path.isfile(fileOrDir):
        if fileOrDir.name.endswith(".pyi"):
            os.remove(fileOrDir)
        elif fileOrDir.name.endswith(".cp312-win_amd64.pyd"):
            targetFilename = fileOrDir.name[:-len(".cp312-win_amd64.pyd")] + ".pyd"
            os.rename(fileOrDir.name, targetFilename)
os.system("move *.pyd bin")

os.chdir("..\\core")
os.makedirs("core", exist_ok=True)
for fileOrDir in os.scandir('.'):
    if os.path.isdir(fileOrDir):
        shutil.rmtree(fileOrDir)
    elif os.path.isfile(fileOrDir):
        if fileOrDir.name.endswith(".pyi"):
            os.remove(fileOrDir)
        elif fileOrDir.name.endswith(".cp312-win_amd64.pyd"):
            targetFilename = fileOrDir.name[:-len(".cp312-win_amd64.pyd")] + ".pyd"
            os.rename(fileOrDir.name, targetFilename)
os.system("move *.pyd core")
