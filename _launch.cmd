@echo off
rem ===== Survival AI common launcher (called by the Start*.bat files) =====
rem Args: 1=model file  2=web UI config  3=context size  4=max reply tokens  5=mode (auto or igpu)  6=library passages per question
setlocal EnableExtensions EnableDelayedExpansion
set "AI=%~dp0"
set "AI=%AI:~0,-1%"
set "APP=%AI%\app"
set "MODEL=%AI%\models\%~1"
set "UICFG=%AI%\config\%~2"
set "CTX=%~3"
set "NPRED=%~4"
set "MODE=%~5"
set "MNAME=%~1"
set "K=%~6"
if "%K%"=="" set "K=4"
set "PORT=8080"
set "URL=http://127.0.0.1:%PORT%"
set "CHATURL=http://127.0.0.1:8081"
if not exist "%AI%\logs" mkdir "%AI%\logs" >nul 2>&1

if not exist "%MODEL%" (
  echo Model file not found: "%MODEL%"
  pause
  exit /b 1
)

curl.exe -sf -m 2 -o nul "%URL%/health" >nul 2>&1
if not errorlevel 1 (
  echo Survival AI is already running.
  echo To switch models, run "Stop Survival AI.bat" first.
  call :startchat
  start "" "!OPENURL!"
  ping -n 6 127.0.0.1 >nul
  exit /b 0
)

rem Threads = physical cores (logical / 2), capped at 8
set /a THREADS=%NUMBER_OF_PROCESSORS%/2
if %THREADS% GTR 8 set THREADS=8
if %THREADS% LSS 1 set THREADS=1

set "ARGS=-m "%MODEL%" --host 127.0.0.1 --port %PORT% -c %CTX% -n %NPRED% -t %THREADS% -tb %THREADS% -np 1 -fa on --reasoning off --temp 0.7 --top-p 0.8 --top-k 20 --min-p 0 --presence-penalty 1.5 --cache-ram 0 --sleep-idle-seconds 300 --offline --cors-origins localhost --ui-config-file "%UICFG%""

rem Backend order: NVIDIA CUDA -> Vulkan (any GPU) -> CPU only
set "ORDER="
if /i "%MODE%"=="igpu" goto :igpu
if exist "%SystemRoot%\System32\nvcuda.dll" set "ORDER=cuda"
if exist "%SystemRoot%\System32\vulkan-1.dll" set "ORDER=%ORDER% vulkan"
set "ORDER=%ORDER% cpu"
goto :try

:igpu
rem Low-power mode: use the built-in (integrated) GPU via Vulkan so the NVIDIA GPU can stay asleep
set "DEV="
"%APP%\vulkan\llama-server.exe" --list-devices > "%AI%\logs\devices.txt" 2>nul
for /f "tokens=1 delims=: " %%D in ('findstr /i "Radeon Intel Iris UHD Arc" "%AI%\logs\devices.txt"') do if not defined DEV set "DEV=%%D"
if defined DEV (
  echo Using integrated GPU device !DEV!
  set "ARGS=!ARGS! --device !DEV!"
  set "ORDER=vulkan cpu"
) else (
  echo No integrated GPU found - using CPU only.
  set "ORDER=cpu"
)

:try
for %%B in (%ORDER%) do (
  echo.
  echo Starting Survival AI with the %%B build ... first load from USB can take 30-90 seconds.
  start "Survival AI server (%%B) - run Stop Survival AI.bat to stop" /min "%APP%\%%B\llama-server.exe" !ARGS! --log-file "%AI%\logs\server-%%B.log"
  call :waitready
  if !READY!==1 (
    echo Survival AI is ready on %URL% using the %%B build.
    call :startchat
    start "" "!OPENURL!"
    echo.
    echo Library Chat ^(answers from your guides, with sources^): %CHATURL%
    echo Plain AI chat ^(no library search, + button attaches a PDF^): %URL%
    echo Leave the minimized server window open while you chat ^(Library Chat runs in the background^).
    echo When finished, double-click "Stop Survival AI.bat" to save battery.
    ping -n 11 127.0.0.1 >nul
    exit /b 0
  )
  echo The %%B build did not start. Trying the next option...
  taskkill /im llama-server.exe /f >nul 2>&1
  ping -n 3 127.0.0.1 >nul
)
echo.
echo Could not start the AI. See the logs folder: "%AI%\logs"
echo The Survival Library PDFs still work without the AI.
pause
exit /b 1

:startchat
rem Starts the Library Chat (portable Python, 127.0.0.1:8081). Falls back to the plain UI if it cannot start.
set "OPENURL=%URL%"
curl.exe -sf -m 2 -o nul "%CHATURL%/api/info" >nul 2>&1
if not errorlevel 1 (
  set "OPENURL=%CHATURL%"
  goto :eof
)
if not exist "%AI%\library-search\index\chunks.json" goto :eof
start "" "%APP%\python\pythonw.exe" "%AI%\library-search\server.py" --port 8081 --k %K% --max-tokens %NPRED% --mode "%MODE% - %MNAME%" --pidfile "%AI%\logs\library-chat.pid"
for /l %%i in (1,1,30) do (
  ping -n 2 127.0.0.1 >nul
  curl.exe -sf -m 2 -o nul "%CHATURL%/api/info" >nul 2>&1
  if not errorlevel 1 (
    set "OPENURL=%CHATURL%"
    goto :eof
  )
)
echo Library Chat did not start - opening the plain AI chat instead.
goto :eof

:waitready
set READY=0
for /l %%i in (1,1,120) do (
  ping -n 2 127.0.0.1 >nul
  curl.exe -sf -m 2 -o nul "%URL%/health" >nul 2>&1
  if not errorlevel 1 (
    set READY=1
    goto :eof
  )
  tasklist /fi "imagename eq llama-server.exe" 2>nul | find /i "llama-server.exe" >nul
  if errorlevel 1 goto :eof
)
goto :eof
