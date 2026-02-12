@echo off
REM Windows launcher for Ghost Shell (Phoenix rebuild)

setlocal ENABLEDELAYEDEXPANSION
set SCRIPT_DIR=%~dp0
set PYTHONUNBUFFERED=1

REM 1) Prefer host python if available
where python >nul 2>&1
if %ERRORLEVEL%==0 (
    cd "%SCRIPT_DIR%src" || goto :eof
    python main.py
    goto :eof
)

REM 2) Fallback to portable Python in bin\python\python.exe
if exist "%SCRIPT_DIR%bin\python\python.exe" (
    cd "%SCRIPT_DIR%src" || goto :eof
    "%SCRIPT_DIR%bin\python\python.exe" main.py
    goto :eof
)

echo [!] No Python found on host and no portable runtime in bin\python.
echo [!] Please install Python or drop a portable runtime into bin\python.
endlocal
