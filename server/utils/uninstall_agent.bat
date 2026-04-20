@echo off
echo Removendo AutoHUB Agent...

cd /d "%~dp0"

nssm stop AutoHUBAgent
nssm remove AutoHUBAgent confirm

rmdir /S /Q "%~dp0"

echo.
echo Removido com sucesso!
pause