@echo off
echo Stopping Survival AI ...
set "STOPPED="
taskkill /im llama-server.exe /f >nul 2>&1
if not errorlevel 1 set "STOPPED=1"
set "PIDF=%~dp0logs\library-chat.pid"
if exist "%PIDF%" (
  for /f "usebackq delims=" %%p in ("%PIDF%") do (
    tasklist /fi "pid eq %%p" 2>nul | find /i "python" >nul && taskkill /pid %%p /f >nul 2>&1 && set "STOPPED=1"
  )
  del "%PIDF%" >nul 2>&1
)
if defined STOPPED (echo Survival AI stopped. GPU and memory are free again.) else (echo Survival AI was not running.)
ping -n 5 127.0.0.1 >nul
