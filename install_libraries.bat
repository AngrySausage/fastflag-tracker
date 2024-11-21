@echo off

set "parent=%~dp0"
set "libraries_path=%parent%\libraries"


if not exist "%libraries_path%" (
    mkdir "%libraries_path%"
)

pip install --upgrade --target="%libraries_path%" requests

pause