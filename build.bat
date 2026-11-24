@echo off
setlocal
cd /d "%~dp0"
py -m pip install -r requirements.txt pyinstaller || exit /b 1
cd frontend
call npm install || exit /b 1
call npm run build || exit /b 1
cd ..
py -m PyInstaller --noconfirm --windowed --onedir --name AutoPulse --add-data "frontend/dist;frontend/dist" --collect-all webview --collect-all uvicorn --collect-all websockets launcher.py || exit /b 1
echo Build complete: dist\AutoPulse\AutoPulse.exe
