@echo off
REM Batch file to start Chrome with remote debugging on Windows

echo Starting Chrome with remote debugging on port 9222...

REM Try common Chrome paths
if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe
    goto :start
)

if exist "%PROGRAMFILES%\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH=%PROGRAMFILES%\Google\Chrome\Application\chrome.exe
    goto :start
)

if exist "%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH=%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe
    goto :start
)

echo Chrome not found! Please edit this file and set CHROME_PATH manually.
pause
exit /b 1

:start
echo Using Chrome at: %CHROME_PATH%

REM Start Chrome with remote debugging and open follower page
start "" "%CHROME_PATH%" --remote-debugging-port=9222 --user-data-dir=%TEMP%\chrome-debug-profile "https://tabelog.com/rvwr/000141867/follower/"

echo.
echo Chrome started with remote debugging!
echo Opening follower page...
echo Please login to Tabelog in the opened Chrome window
echo Then run: python main.py
echo.
pause

