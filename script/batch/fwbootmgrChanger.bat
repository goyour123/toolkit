@REM
@REM fwbootmgrChanger - List all fwbootmgr options and change the boot order
@REM

@echo off

setlocal EnableDelayedExpansion

@REM List all fwbootmgr options
echo fwbootmgr
echo.
set getDes=false
set /a optIdx=0
for /f "tokens=1*" %%a in ('bcdedit /enum firmware') do (
  if "!getDes!" EQU "true" (
    set des=%%b
    set /a optIdx += 1
    set getDes=false
    echo !optIdx!.identifier:          !id! 
    echo   description:          !des!
    echo.
  )

  if "%%a" EQU "identifier" (
    if "%%b" NEQ "{fwbootmgr}" (
      set id=%%b
      set getDes=true
    )
  )
)

@REM Let user to choose which option would boot first
set /p tgtIdx=Choose which option to boot first by entering a number from 1 to %optIdx%:  

@REM Get id of the chosen option
set getDes=false
set /a optIdx=0
for /f "tokens=1*" %%a in ('bcdedit /enum firmware') do (
  if "%%a" EQU "identifier" (
    if "%%b" NEQ "{fwbootmgr}" (
      set /a optIdx += 1
      if "!optIdx!" EQU "%tgtIdx%" (
        set id=%%b
      )
    )
  )
)

echo The chosen identifier: %id%
echo.

bcdedit /set {fwbootmgr} displayorder %id% /addfirst

pause
