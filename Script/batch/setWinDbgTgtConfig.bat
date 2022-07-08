@REM
@REM setWinDbgTgtConfig.bat - Setup WinDbg environment
@REM

@setlocal EnableDelayedExpansion

@echo 1: USB3
@echo 2: Serial Port
@echo 3: Debug turn off
@set /p cnt="Select Connect Type (ex:1 for USB3):"

@if "%cnt%"=="1" (
  @goto USB3
) else if "%cnt%"=="2" (
  @goto SERIAL
) else if "%cnt%"=="3" (
  @goto DBGOFF
) else (
  @echo No Connect Type selected
  @pause
  @exit /b 1
)

:USB3
@REM via USB3
@echo Connecting via USB3
@set /p tgt="Set Target Name (ex:test):"
bcdedit /dbgsettings usb targetname:%tgt%
@set /p bus="Set Bus number (ex:2):"
@set /p dev="Set Dev number (ex:0):"
@set /p func="Set Func number (ex:3):"
bcdedit /set {dbgsettings} busparams %bus%.%dev%.%func%
@goto DONE

:SERIAL
@REM via Serial Port
@echo Connection via Serial Port
@set /p port="Set COM port number (ex:1):"
@set /p baudrate="Set Baud Rate (ex:115200):"
bcdedit /dbgsettings serial debugport:%port% baudrate:%baudrate%
@goto DONE

:DBGOFF
bcdedit /debug off
bcdedit /set testsigning off
@pause
@exit / 0

:DONE
bcdedit /debug on
bcdedit /set testsigning on
@pause
@exit / 0