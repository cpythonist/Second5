# 
# Second 5.0 source code
# 
# Filename          : updater.py
# Brief description : Contains update methods updater() and installer().
# 
# This software is a product of Infinite, Inc., and was written by
# CPythonist (cpythonist.github.io) of the development team of Infinite, Inc.
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
# Please refer http://cpythonist.github.io/second/documentation/secondDoc5.0.html
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
    from packaging.version import parse
    import base64
    import logging
    import requests
    import os
    import psutil
    import shutil
    import tempfile
    import time
    import traceback
    import zipfile
    import globalFile as gn

except (ImportError, FileNotFoundError, ModuleNotFoundError) as e:
    importErr("updater", e)

def installer(pidStr, latVerAvail):
    """
    Function to install updates if updates are available. Called from updater() in the same thread.
    """
    with open("update.txt", 'r', buffering=1) as file:
        # The "try-wrap"
        try:
            # Get version number (i.e., number before first decimal point)
            versionNumber = str(gn.__version__).split('.')[0]
            latVerAvail = str(latVerAvail).split('.')[0]
            
            # Try to make error and output directories, then create handlers for logging into files,
            # then create loggers objects. Two loggers available: one for all output and one for detailing errors.
            os.makedirs("logs", mode=0o777, exist_ok=True)
            handler1 = logging.FileHandler(filename=f"logs{os.sep}installer.log", mode="a")
            handler1.setLevel(logging.DEBUG)
            handler1.setFormatter(logging.Formatter("\n%(asctime)s\n%(levelname)s:%(name)s: %(message)s\n----------------------\n"))
            logger1 = logging.getLogger("installer")
            logger1.addHandler(handler1)

            handler2 = logging.FileHandler(filename="logs{os.sep}installerErr.log", mode="a")
            handler2.setLevel(logging.DEBUG)
            handler2.setFormatter(logging.Formatter("\n%(asctime)s\n%(levelname)s:%(name)s: %(message)s\n----------------------\n"))
            logger2 = logging.getLogger("installerErr")
            logger2.addHandler(handler2)

            if file.read(1) in ('-', '1'):
                oldPath = os.getcwd()
                os.chdir("..")

                # Try to get data
                data = requests.get(f'https://github.com/cpythonist/Second{latVerAvail}/releases/latest/download/Second{latVerAvail}.zip', headers={"Authorization" : 'token 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', "Accept": 'application/vnd.github.v3+json'})

                if data.status_code != 200: # Or log error message and exit
                    logger2.error(f"{data.text}")
                
                # Fetch operation was successful
                with open(f"{tempfile.gettempdir()}{os.sep}Second{latVerAvail}_New.zip", 'wb') as f: # Write .zip file to temporary folder
                    f.write(data.content)
                
                while True:
                    try:
                        if psutil.pid_exists(int(pidStr)):
                            continue
                        gn.customPrint(f"Second {latVerAvail} is available. Do you want to upgrade your program [y]/n ?\n!!~$## ")
                        choice = input().lower()

                        if choice in ('', 'y', 'yes') or choice.isspace():
                            gn.customPrint(f"Upgrading from Second {versionNumber} to Second {latVerAvail}...")
                            with zipfile.ZipFile(f"{tempfile.gettempdir()}{os.sep}Second{latVerAvail}_New.zip", 'r') as f: # Extract .zip file to the install directory
                                f.extractall(os.getcwd())
                            
                            os.remove(f"{tempfile.gettempdir()}{os.sep}Second{latVerAvail}_New.zip") # Delete downloaded zip file in temp dir
                            
                            os.rename(f"Second{latVerAvail}_New", f"Second{latVerAvail}")
                            if os.path.isfile(f"Second{versionNumber}{os.sep}ssettings.dat"):
                                shutil.copy(f"Second{versionNumber}{os.sep}ssettings.dat", f"Second{latVerAvail}{os.sep}ssettings.dat")
                            elif os.path.isfile(f"Second{versionNumber}{os.sep}settings.dat"):
                                shutil.copy(f"Second{versionNumber}{os.sep}settings.dat", f"Second{latVerAvail}{os.sep}ssettings.dat")
                            if os.path.isfile(f"Second{versionNumber}{os.sep}saliases.txt"):
                                shutil.copy(f"Second{versionNumber}{os.sep}saliases.txt", f"Second{latVerAvail}{os.sep}saliases.txt")
                            
                            for i in os.scandir(f"Second{versionNumber}"):
                                try:
                                    if os.path.isfile(i.name):
                                        if i.name.lower() not in ("ssettings.dat", "saliases.txt"):
                                            os.remove(i.name)
                                    elif os.path.isdir(i.name):
                                        if i.name.lower() not in ("bin", "logs", "plugins"):
                                            shutil.rmtree(i.name)
                                except FileNotFoundError:
                                    pass
                                except Exception as e:
                                    gn.customPrint(f"&&UPDATER5:## ??Unknown Error:## {e.__class__.__name__}: {e}\n")
                                    logger2.error(f"An unknown error has occured:\n{e.__class__.__name__}: {e}\n")
                                    return None
                            
                            logger1.info(f"The update was successful.\nInfo:\nUpdated from Second {versionNumber} to Second {latVerAvail}")
                            
                        elif choice in ('n', 'no'):
                            gn.info("updater5", f"User denied upgrade. Second {latVerAvail} was NOT installed", printFunc=True)
                            logger1.info(f"User denied update from Second {versionNumber} to Second {latVerAvail}")
                            with open("update.txt", 'w', buffering=1) as f:
                                f.write("0")
                        
                        else:
                            gn.info("updater5", "Invalid option entered", printFunc=True)
                            with open("update.txt", 'w', buffering=1) as f:
                                f.write("-")
                        
                        time.sleep(1)
                    
                    except Exception as e:
                        logger2.error(f"An unknown error has occured:\n{e.__class__.__name__}: {e}\n")

        except ConnectionError: # If Internet connection is not available
            logger2.error(f"\n\nNo internet connection available.\n{traceback.format_exc()}\n")

        except FileNotFoundError: # If previous installation was not found
            logger2.warning(f"\n\nPrevious installation was not found.\n{traceback.format_exc()}\n")

        except Exception: # Any other exception
            logger2.critical(f"\n\nCritical Exception:\n{traceback.format_exc()}\n")


def updater(pidStr):
    """
    Function to check for updates. Called from main() in a separate thread.
    """
    # The "try-wrap"
    try:
        currentVersion = parse(str(gn.__version__))

        # Get latest version data, i.e. content of text file present in a GitHub repository
        if (latestVersion:=requests.get("https://api.github.com/repos/cpythonist/secondVersionManagement/contents/latestVersion.txt", headers={'Authorization': 'token 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'})).status_code == requests.codes.ok:
            latestVersion = parse(base64.b64decode(latestVersion.json()['content']).decode("utf-8").strip())
            
            if currentVersion < latestVersion: # Determine if update is available
                installer(pidStr, latestVersion)

    except ConnectionError:
        pass

    except Exception as e:
        pass
