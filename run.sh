#!/bin/bash
# Audio Generator App Runner
# This script automatically activates the virtual environment and runs the app

echo "🚀 Starting Audio Generator App..."
echo "📦 Activating virtual environment..."

# Activate virtual environment
source venv/bin/activate

# Check if activation was successful
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Virtual environment activated: $VIRTUAL_ENV"
    echo "🐍 Python version: $(python --version)"
    echo "🌐 Starting Flask app..."
    python app.py
else
    echo "❌ Failed to activate virtual environment"
    echo "💡 Make sure you're in the project directory and venv exists"
    exit 1
fi