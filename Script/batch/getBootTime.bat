
@set year=%date:~0,4%
@set month=%date:~5,2%
@set day=%date:~8,2%

@REM Remove leading zeros
@for /f "tokens=* delims=0" %%a in ("%month%") do @set month=%%a
@for /f "tokens=* delims=0" %%a in ("%day%") do @set day=%%a

@for /f "tokens=1,2,3,4,5,6,7,8 delims=-,/ " %%a in ('systeminfo') do @(
  @if "%%a %%b" == "System Boot" (
    @set boottime="%%d/%%e/%%f, %%g %%h"
    @goto OUTPUTBOOTTIME
  )
  @if %%b equ %year% (
    @if %%c equ %month% (
      @if %%d equ %day% (
        @set boottime="%%b/%%c/%%d, %%e %%f"
        @goto OUTPUTBOOTTIME
      )
    )
  )
)

:OUTPUTBOOTTIME
@pushd "C:\Users\%USERNAME%\Desktop"
@echo %boottime% >> Boot.txt
@popd
