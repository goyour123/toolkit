@REM
@REM char2Ascii.bat
@REM
@REM This batch file would take the ARG1 as input character and echo its ASCII code in
@REM decimal.
@REM

@setlocal EnableDelayedExpansion

@set char=%1
@set ascii=

@for /l %%a in (32,1,126) do @(
  cmd /c exit %%a
  if "!=exitcodeAscii!" EQU "%char%" set ascii=%%a
)
@echo %ascii%
