@echo off
echo === Step 1: Building React frontend ===
cd /d "%~dp0react-frontend"
call npm install
call npm run build
if errorlevel 1 (
    echo React build failed. Aborting.
    pause
    exit /b 1
)

echo === Step 2: Installing Python dependencies ===
cd /d "%~dp0FastAPI"
call env\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller

echo === Step 3: Packaging into executable ===
pyinstaller --onefile --noconsole ^
    --add-data "static;static" ^
    --add-data "models.py;." ^
    --add-data "schemas.py;." ^
    --add-data "crud.py;." ^
    --add-data "database.py;." ^
    --name "ItemsManager" ^
    run.py

echo === Done! ===
echo Executable is at: FastAPI\dist\ItemsManager.exe
echo Make sure PostgreSQL is running before launching it.
pause
