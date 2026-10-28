@echo off
rem Bigger 9B model - better answers, uses more power. Opens the Library Chat (answers cite your guides).
call "%~dp0_launch.cmd" "Qwen_Qwen3.5-9B-Q4_K_M.gguf" "webui-plugged-in.json" 8192 1024 auto 6
