@echo off
REM Windows launcher for Ghost Shell (Phoenix rebuild)

set SCRIPT_DIR=%~dp0
set PYTHONUNBUFFERED=1

cd "%SCRIPT_DIR%src" || goto :eof
python main.py
