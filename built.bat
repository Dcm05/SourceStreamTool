@echo off
REM Set executable name
set EXENAME=SourceStreamTool

REM Clean previous builds (optional)
echo Cleaning old build...
rmdir /s /q build
rmdir /s /q dist
del /q %EXENAME%.spec

REM Build with PyInstaller
echo Building %EXENAME%.exe...
python -m PyInstaller --onefile --name %EXENAME% ^
--icon=logo.ico ^
--add-data "templates;templates" ^
--add-data "static;static" ^
main.py

echo.
echo Build complete! Find your EXE in the /dist folder.
pause
