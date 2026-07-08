@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

set "ROOT_DIR=%~dp0"
if "%ROOT_DIR:~-1%"=="\" set "ROOT_DIR=%ROOT_DIR:~0,-1%"
set "BACKEND_DIR=%ROOT_DIR%\backend"
set "FRONTEND_DIR=%ROOT_DIR%\frontend"

if not defined BACKEND_HOST set "BACKEND_HOST=127.0.0.1"
if not defined BACKEND_PORT set "BACKEND_PORT=8000"
if not defined FRONTEND_HOST set "FRONTEND_HOST=127.0.0.1"
if not defined FRONTEND_PORT set "FRONTEND_PORT=5173"
if not defined SKIP_SETUP set "SKIP_SETUP=0"

echo.
echo EduTrack Pro demo runner
echo ========================

REM ---- Pick free ports (increments if the default is busy) ----
call :choose_port %BACKEND_PORT% BACKEND_PORT
call :choose_port %FRONTEND_PORT% FRONTEND_PORT

REM ---- Backend: venv, deps, .env, seed ----
echo.
echo Preparing backend...

set "BACKEND_PY=%BACKEND_DIR%\venv\Scripts\python.exe"
if not exist "%BACKEND_PY%" set "BACKEND_PY=%BACKEND_DIR%\.venv\Scripts\python.exe"

if not exist "%BACKEND_PY%" (
    if "%SKIP_SETUP%"=="1" (
        echo ERROR: Backend virtual environment was not found. Run setup.bat or unset SKIP_SETUP.
        exit /b 1
    )
    call "%ROOT_DIR%\setup\backend.bat"
    if errorlevel 1 exit /b 1
    set "BACKEND_PY=%BACKEND_DIR%\venv\Scripts\python.exe"
)

if not exist "%BACKEND_PY%" (
    echo ERROR: Backend virtual environment still missing after setup. Aborting.
    exit /b 1
)

if not "%SKIP_SETUP%"=="1" (
    "%BACKEND_PY%" -c "import fastapi, openpyxl, pandas, sqlalchemy, uvicorn" >nul 2>nul
    if errorlevel 1 (
        pushd "%BACKEND_DIR%"
        "%BACKEND_PY%" -m pip install -r requirements.txt
        if errorlevel 1 (
            popd
            exit /b 1
        )
        popd
    )

    if not exist "%BACKEND_DIR%\.env" (
        if exist "%BACKEND_DIR%\.env.example" (
            copy "%BACKEND_DIR%\.env.example" "%BACKEND_DIR%\.env" >nul
        )
    )
)

pushd "%BACKEND_DIR%"
"%BACKEND_PY%" -m app.database.seed
if errorlevel 1 (
    popd
    echo ERROR: Failed to seed demo data.
    exit /b 1
)
popd
echo OK: Backend ready with demo data

REM ---- Frontend: npm install if needed ----
echo.
echo Preparing frontend...

where npm >nul 2>nul
if errorlevel 1 (
    echo ERROR: npm was not found. Install Node.js and npm first.
    exit /b 1
)

if not "%SKIP_SETUP%"=="1" (
    if not exist "%FRONTEND_DIR%\node_modules\.bin\vite.cmd" (
        pushd "%FRONTEND_DIR%"
        call npm install
        if errorlevel 1 (
            popd
            exit /b 1
        )
        popd
    )
)
echo OK: Frontend ready

REM ---- Start backend in its own window ----
echo.
echo Starting backend...
start "EduTrack Backend" cmd /k "cd /d "%BACKEND_DIR%" && "%BACKEND_PY%" -m uvicorn app.main:app --host %BACKEND_HOST% --port %BACKEND_PORT%"

REM ---- Wait for backend to respond ----
set "HEALTH_URL=http://%BACKEND_HOST%:%BACKEND_PORT%/health"
set /a ATTEMPTS=40
set /a COUNT=1

:wait_loop
curl -fsS "%HEALTH_URL%" >nul 2>nul
if not errorlevel 1 (
    echo OK: Backend is responding at %HEALTH_URL%
    goto backend_ready
)
if %COUNT% GEQ %ATTEMPTS% (
    echo ERROR: Backend did not start at %HEALTH_URL%
    call :stop_all
    exit /b 1
)
set /a COUNT+=1
timeout /t 1 /nobreak >nul
goto wait_loop

:backend_ready

REM ---- Start frontend in its own window ----
echo.
echo Starting frontend...
start "EduTrack Frontend" cmd /k "cd /d "%FRONTEND_DIR%" && set VITE_API_BASE_URL=http://%BACKEND_HOST%:%BACKEND_PORT%/api/v1 && npm run dev -- --host %FRONTEND_HOST% --port %FRONTEND_PORT% --strictPort"

echo.
echo EduTrack Pro is running.
echo.
echo Frontend: http://%FRONTEND_HOST%:%FRONTEND_PORT%
echo Backend:  http://%BACKEND_HOST%:%BACKEND_PORT%/docs
echo.
echo Demo accounts:
echo teacher@example.com / Password123
echo student@example.com / Password123
echo.
echo Backend and frontend are running in separate windows.
echo Press any key in THIS window to stop both servers.
pause >nul

call :stop_all
exit /b 0

REM ==========================================================
:choose_port
REM %1 = starting port, %2 = name of variable to update
setlocal enabledelayedexpansion
set "PORT=%~1"
:port_check
netstat -ano | findstr /r /c:":%PORT% .*LISTENING" >nul 2>nul
if not errorlevel 1 (
    set /a PORT+=1
    goto port_check
)
endlocal & set "%~2=%PORT%"
exit /b 0

REM ==========================================================
:stop_all
echo.
echo Stopping backend and frontend...
taskkill /FI "WINDOWTITLE eq EduTrack Backend*" /T /F >nul 2>nul
taskkill /FI "WINDOWTITLE eq EduTrack Frontend*" /T /F >nul 2>nul
exit /b 0