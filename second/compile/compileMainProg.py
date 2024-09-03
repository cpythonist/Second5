import os

os.chdir("..")
os.system('\
python -OO -m nuitka --standalone --deployment --follow-imports --mingw64 --warn-unusual-code \
--include-module=getpass --include-module=packaging.version --include-module=requests --include-module=psutil -\
-windows-icon-from-ico=icons\\second5.ico --company-name="Infinite Inc." --product-name="Second 5.0" \
--file-version=1.0.0.0 --product-version=5.0 --file-description="The Second 5 Interpreter" --copyright="Apache-2.0" \
--include-data-files=ssettings.dat=.\\ssettings.dat --include-data-files=saliases.txt=.\\saliases.txt second5.py\
')
