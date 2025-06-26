@echo off
echo ========================================
echo vcpkg Dependency Query Tool - Setup
echo ========================================
echo.

echo Checking if Python is installed...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python first.
    echo Visit https://www.python.org/downloads/ to download and install Python
    pause
    exit /b 1
)

echo [OK]Python is installed
echo.

echo Installing required Python packages...
pip install -r requirements.txt

if errorlevel 1 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [OK] All dependencies installed successfully!
echo.
pause 