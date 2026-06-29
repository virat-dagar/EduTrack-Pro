@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%.."
set "FRONTEND_DIR=%ROOT_DIR%\frontend"

where npm >nul 2>nul
if errorlevel 1 (
    echo ERROR: npm is required. Please install Node.js and npm.
    exit /b 1
)

cd /d "%FRONTEND_DIR%"

echo Installing frontend dependencies...
npm install
if errorlevel 1 exit /b 1
echo ✔ Frontend dependencies installed

if "%RUN_NPM_AUDIT_FIX%"=="1" (
    echo Running npm audit fix...
    npm audit fix
    if errorlevel 1 exit /b 1
    echo ✔ npm audit fix complete
) else (
    echo ✔ Skipping npm audit fix
)

echo =================================
echo EduTrack Pro Frontend Ready 🚀
echo Run:
echo npm run dev
echo =================================

if not "%SKIP_FRONTEND_DEV%"=="1" (
    npm run dev
)
