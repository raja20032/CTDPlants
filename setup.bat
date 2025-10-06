@echo off
echo 🌱 Setting up Garden Paradise Plant Shop...

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python is not installed. Please install Python first.
    pause
    exit /b 1
)

REM Install requirements
echo 📦 Installing dependencies...
pip install -r requirements.txt

echo ✅ Setup complete!
echo.
echo 🚀 To run the application:
echo    streamlit run app.py
echo.
echo 📝 Available coupon codes:
echo    - WELCOME10 (10% off)
echo    - SPRING20 (20% off)
echo    - SAVE5 (5% off)
echo    - GARDEN25 (25% off)
echo    - NEWCUSTOMER (15% off)
pause
