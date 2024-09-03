import os
import glob

pydModules = glob.glob(os.path.join("bin", "*.pyd"))
pyModules = glob.glob(os.path.join("bin", "*.py"))

__all__ = [os.path.basename(pydMod)[:-4] for pydMod in pydModules if os.path.isfile(pydMod) and not pydMod.endswith("__init__.pyd")] + \
    [os.path.basename(pyMod)[:-3] for pyMod in pyModules if os.path.isfile(pyMod) and not pyMod.endswith("__init__.py")]
