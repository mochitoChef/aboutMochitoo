@echo off
echo.
echo ==========================================
echo   PORTFOLIO WEBSITE - ALTERNATIVE SERVER
echo ==========================================
echo.

cd /d "%~dp0\portfolio_clone"

echo 📁 Current directory: %CD%
echo 📋 Files in portfolio_clone:
dir /b

echo.
echo 🚀 Starting Python HTTP server on port 8080...
echo 🌐 Website will be available at: http://localhost:8080
echo ⌨️  Press Ctrl+C to stop the server
echo.

python -m http.server 8080

pause
