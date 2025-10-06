# Let's also create a simple setup script for easy installation
setup_script = '''#!/bin/bash

echo "🌱 Setting up Garden Paradise Plant Shop..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "🚀 To run the application:"
echo "   streamlit run app.py"
echo ""
echo "📝 Available coupon codes:"
echo "   - WELCOME10 (10% off)"
echo "   - SPRING20 (20% off)"
echo "   - SAVE5 (5% off)"
echo "   - GARDEN25 (25% off)"
echo "   - NEWCUSTOMER (15% off)"
'''

with open('setup.sh', 'w') as f:
    f.write(setup_script)

# Create a Windows batch file version too
setup_bat = '''@echo off
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
'''

with open('setup.bat', 'w') as f:
    f.write(setup_bat)

print("Created setup scripts:")
print("- setup.sh (for Linux/Mac)")
print("- setup.bat (for Windows)")
print("\n🎉 Complete Garden Paradise Plant Shop application is ready!")

# Show the file structure
print("\n📁 File Structure:")
print("garden-paradise-shop/")
print("├── app.py                 # Main Streamlit application")
print("├── plants_data.json       # Plant inventory data")
print("├── coupons.json          # Coupon codes configuration")
print("├── requirements.txt       # Python dependencies")
print("├── README.md             # Documentation")
print("├── setup.sh              # Setup script (Linux/Mac)")
print("└── setup.bat             # Setup script (Windows)")

print("\n🚀 Quick Start:")
print("1. Install Streamlit: pip install streamlit")
print("2. Run the app: streamlit run app.py")
print("3. Open browser to http://localhost:8501")