@echo off
rem Small 4B model - lowest battery use. Opens the Library Chat (answers cite your guides).
call "%~dp0_launch.cmd" "Qwen3.5-4B-Q4_K_M.gguf" "webui-battery.json" 4096 512 auto 4
