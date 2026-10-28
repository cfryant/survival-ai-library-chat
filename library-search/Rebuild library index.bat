@echo off
rem Re-reads every PDF in "Survival Library" (run this after adding or changing guides).
cd /d "%~dp0"
echo Rebuilding the Survival Library search index - this takes about a minute...
"%~dp0..\app\python\python.exe" "%~dp0build_index.py"
"%~dp0..\app\python\python.exe" "%~dp0make_prompt.py"
echo Done. Restart Survival AI to use the new index.
pause
