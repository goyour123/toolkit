@REM
@REM getFwPOSTTime.bat - Get firmware POST time under Windows system
@REM
@REM Extract FwPOSTTime and POSTTime from HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Power
@REM register under Windows system.
@REM

@echo off
start /wait regedit.exe /e %cd%\tmp.txt "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Power"

for /f "tokens=2 delims=:" %%a in ('find "FwPOSTTime" %cd%\tmp.txt') do set fwposttime_hex=0x%%a
for /f "tokens=2 delims=:" %%a in ('find "POSTTime" %cd%\tmp.txt') do set posttime_hex=0x%%a

set /a fwposttime_dec=%fwposttime_hex%
set /a posttime_dec=%posttime_hex%

echo FwPOSTTime %fwposttime_hex%(%fwposttime_dec%)
echo POSTTime %posttime_hex%(%posttime_dec%)

del /q %cd%\tmp.txt
pause