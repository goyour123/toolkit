@REM
@REM BuildEdk2.bat - Setup EDK2 build environment
@REM

@echo off

@setlocal EnableDelayedExpansion

set EDK_DRIVE=%~d0
set EDK_WORKSPACE=%CD%
set EDK_REPO=edk2

set PYTHON_HOME=C:\Python27
set CYGWIN_HOME=C:\cygwin64

set QEMU_HOME=C:\Program Files\qemu
@for /f "delims=\ tokens=1" %%a in ("%QEMU_HOME%") do @set QEMU_DRIVE=%%a

@REM set EDK_TOOLS_BIN=%EDK_WORKSPACE%\edk2-BaseTools-win32
set NASM_PREFIX=%EDK_WORKSPACE%\nasm-2.16.03\
set IASL_PREFIX=%EDK_WORKSPACE%\iasl-win-20241212\

cd %EDK_WORKSPACE%\%EDK_REPO%\


@REM Package build setting
set BUILD_TOOL_CHAIN=VS2019
set BUILD_ARCH=IA32 X64
set BUILD_TARGET=DEBUG
set BUILD_OPTIONS=

@for %%a in (%BUILD_ARCH%) do @set BUILD_ARCH_OPTIONS=!BUILD_ARCH_OPTIONS! -a %%a

@REM OVMF setting
@REM OVMF_OPTION=EFI_DEBUG or SOURCE_DEBUG
set OVMF_OPTION=EFI_DEBUG
@if "%OVMF_OPTION%" == "EFI_DEBUG" (
  set "OVMF_BUILD_OPTIONS=-D NETWORK_ENABLE=FALSE -D DEBUG_ON_SERIAL_PORT"
) else if "%OVMF_OPTION%" == "SOURCE_DEBUG" (
  set "OVMF_BUILD_OPTIONS=-D NETWORK_ENABLE=FALSE -D SOURCE_DEBUG_ENABLE=TRUE -D DEBUG_ON_SERIAL_PORT"
) else (
  set "OVMF_BUILD_OPTIONS=-D NETWORK_ENABLE=FALSE -D DEBUG_ON_SERIAL_PORT"
)
@if "%BUILD_ARCH%" == "IA32 X64" (
  set OVMF_BUILD=Ovmf3264
  set OVMF_DSC=OvmfPkgIa32X64
) else (
  set OVMF_BUILD=OvmfX64
  set OVMF_DSC=OvmfPkgX64
)

@REM Gen 123IVPkg.bat
echo build -p 123IVPkg\123IVPkg.dsc -t %BUILD_TOOL_CHAIN% -b %BUILD_TARGET% %BUILD_ARCH_OPTIONS% > %cd%\Build123IVPkg.bat

@REM Gen BuildEmulator.bat
echo build -p EmulatorPkg\EmulatorPkg.dsc -t %BUILD_TOOL_CHAIN% -b %BUILD_TARGET% -a X64 > %cd%\BuildEmulator.bat

@REM Gen BuildOvmf.bat
set "BUILD_OPTIONS=%OVMF_BUILD_OPTIONS% %BUILD_OPTIONS%"
echo build -p OvmfPkg\%OVMF_DSC%.dsc -t %BUILD_TOOL_CHAIN% -b %BUILD_TARGET% %BUILD_ARCH_OPTIONS% %BUILD_OPTIONS%> %cd%\BuildOvmf.bat

@REM Gen RunEmulator.bat
echo pushd %cd%\Build\EmulatorX64\%BUILD_TARGET%_%BUILD_TOOL_CHAIN%\X64 > %cd%\RunEmulator.bat
echo %cd%\Build\EmulatorX64\%BUILD_TARGET%_%BUILD_TOOL_CHAIN%\X64\WinHost.exe >> %cd%\RunEmulator.bat
echo popd >> %cd%\RunEmulator.bat

@REM Gen RunOvmf.bat
@set RUN_OVMF_SCRIPT=%cd%\RunOvmf.bat
@set FS_DIR=%EDK_WORKSPACE%\%EDK_REPO%\Build\%OVMF_BUILD%\%BUILD_TARGET%_%BUILD_TOOL_CHAIN%\X64

echo @set OVMF_BIOS=%EDK_WORKSPACE%\%EDK_REPO%\Build\%OVMF_BUILD%\%BUILD_TARGET%_%BUILD_TOOL_CHAIN%\FV\OVMF.fd > %RUN_OVMF_SCRIPT%
echo @set FS_DIR=%FS_DIR% >> %cd%\RunOvmf.bat
echo @set "QEMU_ARG=-bios %%OVMF_BIOS%%" >> %cd%\RunOvmf.bat
echo @if not "%%FS_DIR%%" == "" ( >> %cd%\RunOvmf.bat
echo   @set "QEMU_ARG=-hda fat:rw:%%FS_DIR%% %%QEMU_ARG%%"  >> %cd%\RunOvmf.bat
echo ) >> %cd%\RunOvmf.bat
@if "%OVMF_OPTION%" == "EFI_DEBUG" (
  echo @set "QEMU_ARG=-serial COM3 %%QEMU_ARG%%" >> %cd%\RunOvmf.bat
) else if "%OVMF_OPTION%" == "SOURCE_DEBUG" (
  echo @set "QEMU_ARG=-serial tcp:localhost:20716,server %%QEMU_ARG%%" >> %cd%\RunOvmf.bat
) else (
  echo @set "QEMU_ARG=-debugcon file:debug.log -global isa-debugcon.iobase=0x402 %%QEMU_ARG%%" >> %cd%\RunOvmf.bat
)

echo @pushd %QEMU_HOME% >> %cd%\RunOvmf.bat
echo %QEMU_DRIVE% >> %cd%\RunOvmf.bat
echo qemu-system-x86_64.exe %%QEMU_ARG%% >> %cd%\RunOvmf.bat
echo @popd >> %cd%\RunOvmf.bat
echo %EDK_DRIVE% >> %cd%\RunOvmf.bat

call edksetup.bat
cmd
