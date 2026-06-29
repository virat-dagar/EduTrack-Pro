@echo off
setlocal
chcp 65001 >nul

set "ROOT_DIR=%~dp0"

echo ====================================
echo EduTrack Pro Setup
echo 1. Backend
echo 2. Frontend
echo 3. Complete Project
echo Choose:
echo ====================================
set /p CHOICE=

if "%CHOICE%"=="1" (
    call "%ROOT_DIR%setup\backend.bat"
    exit /b %ERRORLEVEL%
)

if "%CHOICE%"=="2" (
    call "%ROOT_DIR%setup\frontend.bat"
    exit /b %ERRORLEVEL%
)

if "%CHOICE%"=="3" (
    call "%ROOT_DIR%setup\backend.bat"
    if errorlevel 1 exit /b 1
    set "SKIP_FRONTEND_DEV=1"
    call "%ROOT_DIR%setup\frontend.bat"
    if errorlevel 1 exit /b 1
    echo ====================================
    echo EduTrack Pro Setup Complete 🚀
    echo Run backend:
    echo cd backend ^&^& venv\Scripts\activate ^&^& uvicorn app.main:app --reload
    echo.
    echo Run frontend:
    echo cd frontend ^&^& npm run dev
    echo ====================================
    exit /b 0
)

echo Invalid choice. Please choose 1, 2, or 3.
exit /b 1
