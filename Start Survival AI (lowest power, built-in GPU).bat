@echo off
rem 4B model on the built-in (integrated) GPU via Vulkan - lets a discrete GPU sleep.
call "%~dp0_launch.cmd" "Qwen3.5-4B-Q4_K_M.gguf" "webui-battery.json" 4096 512 igpu 4
