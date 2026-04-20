@echo off
echo Instalando AutoHUB Agent...

:: Caminho onde o agent será instalado
set INSTALL_DIR=C:\AutoHUBAgent

cd /d "%~dp0"

mkdir %INSTALL_DIR%

:: Copiar pasta
robocopy AutoHubAgent %INSTALL_DIR% /E

cd %INSTALL_DIR%

:: Criar serviço com NSSM
nssm install AutoHUBAgent %INSTALL_DIR%\autohub_agent.exe
nssm start AutoHUBAgent

echo.
echo Instalacao concluida!
pause