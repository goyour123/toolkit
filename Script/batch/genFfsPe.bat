@setlocal enabledelayedexpansion

@rem Set UEFIReplace tool path
@set uefireplace_path=%~dp0
@rem Set GenSec tool path
@set gensec_path=..\..\..\BaseTools\Bin\Win32

@rem Set Recovery region offset and size
@set /a recvyoffset=0x1000000+0x83A000
@set /a recvysize=0x120000
@set /a recvyend=%recvyoffset%+%recvysize%

@rem Get the name of rom file
@set romdir=%cd%\BIOS
@pushd !romdir!
@for /f "delims=" %%a in ('dir /b *.fd') do @(
  @set biosname=%%~na
  @set biossize=%%~za
  @goto ROMDONE
)
:ROMDONE
@popd
@echo Rom file name: %biosname%
@echo Rom file size: %biossize%

@rem Get system time for naming
@for /f "tokens=1,2,3 delims=/" %%a in ("%date:~0,10%") do @(
  @set subname=%%b%%c
)
@for /f "tokens=1,2,3 delims=: " %%a in ("%time:~0,8%") do @(
  @set subname=%subname%%%a%%b%%c
)

@rem Check the arguments
@if /i [%1] == [nmake] (
  @start /b /wait cmd.exe /c %1 %2 %3
  @if !errorlevel! neq 0 (
    @goto ERROR
  ) else (
    @echo Build process done
    @goto GENPE
  )
)
@if /i [%1] == [-recvy] (
  @if not exist %romdir%\recvy.fd (
    @echo recvy.fd not found
    goto ERROR
  ) else (
    @if [%biossize%] gtr [%recvyend%] (
      start /b /wait ..\..\..\BaseTools\Bin\Win32\split.exe -f %romdir%\%biosname%.fd -s %recvyoffset% -p %romdir% -o tempromprt1.fd -t temp1.fd
      start /b /wait ..\..\..\BaseTools\Bin\Win32\split.exe -f %romdir%\temp1.fd -s %recvysize% -p %romdir% -o temp2.fd -t tempromprt2.fd
      copy /b /y %romdir%\tempromprt1.fd+%romdir%\recvy.fd %romdir%\temprom.fd
      copy /b /y %romdir%\temprom.fd+%romdir%\tempromprt2.fd %romdir%\%biosname%_%subname%.fd
    ) else (
      start /b /wait ..\..\..\BaseTools\Bin\Win32\split.exe -f %romdir%\%biosname%.fd -s %recvyoffset% -p %romdir% -o tempromprt1.fd -t temp1.fd
      copy /b /y %romdir%\tempromprt1.fd+%romdir%\recvy.fd %romdir%\%biosname%_%subname%.fd
    )
    @del /q %romdir%\temp*.fd
    goto END
  )
)

:GENPE
@rem Get build arch
@for /f "tokens=3" %%a in ('findstr /c:"ARCH =" %3') do @set arch=%%a

@rem Get pe file name
@for /f "tokens=3" %%a in ('findstr /c:"MODULE_NAME =" %3') do @set pename=%%a

@rem Get mudule GUID
@for /f "tokens=3" %%a in ('findstr /c:"MODULE_GUID =" %3') do @set mdlguid=%%a

@echo IMAGE: %pename%
@echo ARCH:  %arch%
@echo GUID:  %mdlguid%

@if /i [%arch%] == [IA32] (
  @echo genFfsPe IA32 process

  @rem Extract Recovery region
  @if [%biossize%] gtr [%recvyend%] (
    start /b /wait ..\..\..\BaseTools\Bin\Win32\split.exe -f %romdir%\%biosname%.fd -s %recvyoffset% -p %romdir% -o temp.fd -t temp2.fd
    start /b /wait ..\..\..\BaseTools\Bin\Win32\split.exe -f %romdir%\temp2.fd -s %recvysize% -p %romdir% -o recvyorg.fd -t temp3.fd
  ) else (
    start /b /wait ..\..\..\BaseTools\Bin\Win32\split.exe -f %romdir%\%biosname%.fd -s %recvyoffset% -p %romdir% -o temp.fd -t recvyorg.fd
  )
  @del /q %romdir%\temp*.fd
) else (
  @echo genFfsPe X64 process
)

@rem Gernerating the ffs
@set efipath=%~dp3OUTPUT
%gensec_path%\GenSec.exe -s EFI_SECTION_PE32 -o %romdir%\%pename%_%subname%_pe.sct %efipath%\%pename%.efi
@if %errorlevel% neq 0 (
  @goto ERROR
) else (
  @echo %romdir%\%pename%_%subname%_pe.sct
  %uefireplace_path%\UEFIReplace.exe %romdir%\%biosname%.fd %mdlguid% 10 %efipath%\%pename%.efi -o %romdir%\%biosname%_%subname%.fd
  @goto END
)

:ERROR
@echo FAILED!!!
@exit /b

:END
@exit /b
