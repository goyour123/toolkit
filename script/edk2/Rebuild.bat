@REM
@REM Rebuild.bat - Rebuild edk base tool
@REM

@echo off

set EDK_WORKSPACE=%CD%
set EDK_REPO=edk2

@REM set PYTHON_HOME=C:\Python27
set CYGWIN_HOME=C:\cygwin64

set NASM_PREFIX=%EDK_WORKSPACE%\nasm-2.15.05\

pushd %EDK_WORKSPACE%\%EDK_REPO%\

call edksetup.bat Rebuild
popd
cmd
