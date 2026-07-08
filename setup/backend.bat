@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%.."
set "BACKEND_DIR=%ROOT_DIR%\backend"

echo Checking Python...
set "PYTHON_CMD="

where py >nul 2>nul
if not errorlevel 1 (
    py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)" >nul 2>nul
    if not errorlevel 1 set "PYTHON_CMD=py -3"
)

if not defined PYTHON_CMD (
    where python >nul 2>nul
    if not errorlevel 1 (
        python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)" >nul 2>nul
        if not errorlevel 1 set "PYTHON_CMD=python"
    )
)

if not defined PYTHON_CMD (
    echo ERROR: Python ^>= 3.11 is required. Please install Python 3.11 or newer.
    exit /b 1
)

for /f "delims=" %%V in ('%PYTHON_CMD% -c "import platform; print(platform.python_version())"') do set "PYTHON_VERSION=%%V"
echo ✔ Python %PYTHON_VERSION% found

cd /d "%BACKEND_DIR%"

echo Creating virtual environment...
if not exist "venv" (
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 exit /b 1
    echo ✔ Virtual environment created
) else (
    echo ✔ Virtual environment already exists
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 exit /b 1
echo ✔ Activated

echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 exit /b 1
echo ✔ pip upgraded

echo Installing dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 exit /b 1
echo ✔ Production dependencies installed

echo Installing development dependencies...
python -m pip install -r requirements-dev.txt
if errorlevel 1 exit /b 1
echo ✔ Development dependencies installed

echo Creating .env...
if not exist ".env" (
    copy ".env.example" ".env" >nul
    echo ✔ .env created
) else (
    echo ✔ .env already exists
)

echo Alembic initialization will be added later.
echo =================================
echo EduTrack Pro Backend Ready 🚀
echo Run:
echo uvicorn app.main:app --reload
echo =================================