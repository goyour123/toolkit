@REM
@REM BuildEdk2.bat - Setup EDK2 build environment
@REM

@echo off

set EDK_DRIVE=%~d0
set EDK_WORKSPACE=%CD%
set EDK_REPO=edk2

set PYTHON_HOME=C:\Python27
set CYGWIN_HOME=C:\cygwin64

set QEMU_HOME=C:\Program Files\qemu
@for /f "delims=\ tokens=1" %%a in ("%QEMU_HOME%") do @set QEMU_DRIVE=%%a

@REM set EDK_TOOLS_BIN=%EDK_WORKSPACE%\edk2-BaseTools-win32
set NASM_PREFIX=%EDK_WORKSPACE%\nasm-2.15.05\
set IASL_PREFIX=%EDK_WORKSPACE%\iasl-win-20210930\

cd %EDK_WORKSPACE%\%EDK_REPO%\


@REM Package build setting
set BUILD_TOOL_CHAIN=VS2019
set BUILD_ARCH=X64
set BUILD_TARGET=RELEASE
set BUILD_OPTIONS=

@REM Gen 123IVPkg.bat
echo build -p 123IVPkg\123IVPkg.dsc -t %BUILD_TOOL_CHAIN% -a %BUILD_ARCH% -b %BUILD_TARGET% > %cd%\Build123IVPkg.bat

@REM Gen BuildEmulator.bat
echo build -p EmulatorPkg\EmulatorPkg.dsc -t %BUILD_TOOL_CHAIN% -a %BUILD_ARCH% -b %BUILD_TARGET% > %cd%\BuildEmulator.bat

@REM Gen BuildOvmf.bat
@if "%BUILD_TARGET%" == "NOOPT" (
  set "BUILD_OPTIONS=-D NETWORK_ENABLE=FALSE -D SOURCE_DEBUG_ENABLE=TRUE -D DEBUG_ON_SERIAL_PORT"
) else (
  set "BUILD_OPTIONS=-D NETWORK_ENABLE=FALSE"
)
echo build -p OvmfPkg\OvmfPkgX64.dsc -t %BUILD_TOOL_CHAIN% -a %BUILD_ARCH% -b %BUILD_TARGET% %BUILD_OPTIONS%> %cd%\BuildOvmf.bat

@REM Gen RunEmulator.bat
echo pushd %cd%\Build\Emulator%BUILD_ARCH%\%BUILD_TARGET%_%BUILD_TOOL_CHAIN%\%BUILD_ARCH% > %cd%\RunEmulator.bat
echo %cd%\Build\Emulator%BUILD_ARCH%\%BUILD_TARGET%_%BUILD_TOOL_CHAIN%\%BUILD_ARCH%\WinHost.exe >> %cd%\RunEmulator.bat
echo popd >> %cd%\RunEmulator.bat

@REM Gen RunOvmf.bat
@set RUN_OVMF_SCRIPT=%cd%\RunOvmf.bat
@set FS_DIR=%EDK_WORKSPACE%\%EDK_REPO%\Build\Ovmf%BUILD_ARCH%\%BUILD_TARGET%_%BUILD_TOOL_CHAIN%\X64

echo @set OVMF_BIOS=%EDK_WORKSPACE%\%EDK_REPO%\Build\Ovmf%BUILD_ARCH%\%BUILD_TARGET%_%BUILD_TOOL_CHAIN%\FV\OVMF.fd > %RUN_OVMF_SCRIPT%
echo @set FS_DIR=%FS_DIR% >> %cd%\RunOvmf.bat
echo @set "QEMU_ARG=-bios %%OVMF_BIOS%%" >> %cd%\RunOvmf.bat
echo @if not "%%FS_DIR%%" == "" ( >> %cd%\RunOvmf.bat
echo   @set "QEMU_ARG=-hda fat:rw:%%FS_DIR%% %%QEMU_ARG%%"  >> %cd%\RunOvmf.bat
echo ) >> %cd%\RunOvmf.bat
@if "%BUILD_TARGET%" == "NOOPT" (
echo @set "QEMU_ARG=-serial tcp:localhost:20716,server %%QEMU_ARG%%" >> %cd%\RunOvmf.bat
)

echo @pushd %QEMU_HOME% >> %cd%\RunOvmf.bat
echo %QEMU_DRIVE% >> %cd%\RunOvmf.bat
echo qemu-system-x86_64.exe %%QEMU_ARG%% >> %cd%\RunOvmf.bat
echo @popd >> %cd%\RunOvmf.bat
echo %EDK_DRIVE% >> %cd%\RunOvmf.bat

call edksetup.bat
cmd
