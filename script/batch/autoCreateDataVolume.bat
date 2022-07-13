@REM
@REM autoCreateDataVolume.bat
@REM
@REM This batch file would auto-create a volume named DATA with letter D from the volume with 
@REM letter C, and the letter D volume would consume half-size space of the letter C volume.
@REM This file is needed to be run as administrator.
@REM

@setlocal EnableDelayedExpansion

@REM Create diskpart script dpSrc.txt for getting volume infomation.
@echo list volume > %~dp0dpSrc.txt

@REM Check whether the Data volume exist or not.
@echo Check whether the Data volume exist or not...
@for /f "tokens=2-4" %%b in ('diskpart /s %~dp0dpSrc.txt^|findstr /c:" D "') do @(
  if /i %%d == DATA (
    @echo Volume D named DATA already exist!
    goto END
  )
  
  @REM The letter D is occupied by other volume.
  if /i %%c == D (
    set volRmLtrNum=%%b
  )
)

@REM Letter D is occupied by other volume.
@if defined volRmLtrNum @(
  @REM Collect the letters of volumes.
  @echo Collect the letters of volumes...
  @set ltr=
  @for /f "tokens=2-4" %%b in ('diskpart /s %~dp0dpSrc.txt^|findstr /r /c:" [C-Z] "') do @(
    set ltr=%%c !ltr!
  )
  @echo Letter used: !ltr!

  @REM Assume the largest leter would not be smaller than C
  @set lgLtr=C
  @set lgLtrAsc=67
  @set ltr2Asn=
  @set ltr2AsnAsc=

  @REM Find largest letter and use the next letter to assign.
  @echo Find largest letter and use the next letter to assign...
  @for %%a in (!ltr!) do @(
    @for /l %%b in (65,1,90) do @(
      cmd /c exit %%b
      if "!=exitcodeAscii!" EQU "%%a" (set asc=%%b)
      if "!asc!" GTR "!lgLtrAsc!" (
      set lgLtr=%%a
      set lgLtrAsc=%%b
      )

      set /a "ltr2AsnAsc=!lgLtrAsc!+1"
      if %%b==!ltr2AsnAsc! (
        set ltr2Asn=!=exitcodeAscii!
      )
    )
  )
  @echo Largest Letter: !lgLtr!
  @echo Letter to Assign: !ltr2Asn!
)

@REM Get number and size of the volume with letter C.
@echo Get the volume number with letter C...
@echo list volume > %~dp0dpSrc.txt
@for /f "tokens=2-6" %%b in ('diskpart /s %~dp0dpSrc.txt^|findstr /c:" C "') do @(
  if /i %%c == C (
    set cVolNum=%%b
    set cVolSize=%%f
  )
)
@echo C volume number: %cVolNum%
@echo C volume size: %cVolSize% GB

@REM Use half-size of letter C space for new volume.
@set /a "dVolSizeGb=%cVolSize%/2"
@set /a "dVolSize=dVolSizeGb*1000"
@echo New D volume size to assign: %dVolSizeGb% GB

@REM Check shrink querymax of volume C.
@echo select volume %cVolNum% > %~dp0dpSrc.txt
@echo shrink querymax >> %~dp0dpSrc.txt
@for /f "tokens=8" %%a in ('diskpart /s %~dp0dpSrc.txt') do @( 
  set cQuerymax=%%a
  @echo Volume C Querymax: !cQuerymax! GB
)
@if "%dVolSize%" GTR "%cQuerymax%" (
  @echo Shrinking size for new volume is greater than C volume querymax^^!^^!^^!
  @goto END
)

@if defined volRmLtrNum (
  @REM Remove the letter D from the occupied volume.
  @echo Remove the letter D from the occupied volume...
  @echo select volume %volRmLtrNum% > %~dp0dpSrc.txt
  @echo remove letter=D >> %~dp0dpSrc.txt
  @echo assign letter=!ltr2Asn! >> %~dp0dpSrc.txt
  diskpart /s %~dp0dpSrc.txt
)

@REM Rewrite the diskpart script dpSrc.txt again for creating volume.
@echo select volume %cVolNum% > %~dp0dpSrc.txt
@echo shrink desired=%dVolSize% >> %~dp0dpSrc.txt
@echo select disk 0 >> %~dp0dpSrc.txt
@echo create partition primary size=%dVolSize% >> %~dp0dpSrc.txt
diskpart /s %~dp0dpSrc.txt

@REM Rewrite the diskpart script dpSrc.txt for getting volume infomation again.
@echo list volume > %~dp0dpSrc.txt

@REM Get the index number of new volume
@for /f "tokens=2" %%b in ('diskpart /s %~dp0dpSrc.txt^|findstr /c:" RAW "') do @(
  set dVolNum=%%b
)

@REM Format the new volume and assign letter D to it.
@echo select volume %dVolNum% > %~dp0dpSrc.txt
@echo format quick fs=ntfs label="DATA" >> %~dp0dpSrc.txt
@echo assign letter=D >> %~dp0dpSrc.txt
diskpart /s %~dp0dpSrc.txt

:END
@REM Delete dpSrc.txt after execution.
@del /q %~dp0dpSrc.txt
@pause
@exit /b 0