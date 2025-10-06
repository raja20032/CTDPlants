#!/bin/bash

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
