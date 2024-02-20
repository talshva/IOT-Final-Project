@echo off
REM Stop Mosquitto service after Python script execution
sc stop mosquitto
if %errorlevel% neq 0 (
    echo Failed to stop Mosquitto service. Ensure you have the necessary permissions.
)
pause
