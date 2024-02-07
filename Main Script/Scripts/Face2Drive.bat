@echo off

REM Start Mosquitto service
sc start mosquitto
if %errorlevel% neq 0 (
    echo Failed to start Mosquitto service. Ensure it is installed and you have the necessary permissions.
    pause
    exit /b %errorlevel%
)

REM Change directory and run Python script
cd C:\Users\Tal Shvartzberg\Desktop\IOT\Main
python main.py


pause
