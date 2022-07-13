@REM
@REM 7zpack.bat - Use 7-Zip to pack a archive without exclude files listed in 7zpack.ini
@REM
@REM This 7zpack.bat consumes ARG1 as the archive to pack and the ARG1 can 
@REM use absolute path and relative path to this batch file. ARG2 is an optional
@REM argument used as output path. If ARG2 was not given, the output archive
@REM will be placed in the same directory as the batch file.
@REM

@REM Set 7z.exe location to zpath variable
@set zpath="C:\Program Files\7-Zip"

@REM Check whether the arg1 is an absolute path or not
@for /f "delims=\ tokens=1" %%a in ("%1") do @(
    if %%a == C: set drive=C:
    if %%a == D: set drive=D:
    if %%a == E: set drive=E:
    if %%a == F: set drive=F:
    if %%a == G: set drive=G:
    if %%a == H: set drive=H:
)

@set folder=%1
@if not defined drive (
    @set folder=%cd%\%1\
)

@set ignore=%cd%\7zpack.ini
@set ignoreRcsv=%cd%\7zpackRcsv.ini

@REM Extract the last item in folder path
@set looppath=%folder%
:lastitemloop
@for /f "delims=\ tokens=1*" %%a in ("%looppath%") do @(
    @set zname=%%a
    @set looppath=%%b
    goto lastitemloop
)

@REM Change path to target path
@%drive%
@cd %folder%

@REM Set 2nd parameter to the output folder
@set dest=%2
if "%dest%" == "" (
    @set dest=%~dp0
)

start cmd.exe /c "%zpath%\7z.exe" a -xr@%ignoreRcsv% -x@%ignore% %dest%%zname%.7z

@%~d0
@cd %~p0
