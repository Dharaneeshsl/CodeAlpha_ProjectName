#!/bin/bash

echo "🚀 Language Translation Tool"
echo "=========================="
echo ""
echo "Option 1: Open in browser (recommended)"
echo "- Open language_translation_tool.html in your web browser"
echo ""
echo "Option 2: Start backend server"
read -p "Press Enter to start the Flask server, or Ctrl+C to exit..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    exit 1
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Setting up virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo "🌐 Starting translation server..."
echo "Server will be available at: http://localhost:5000"
echo "Health check: http://localhost:5000/health"
echo "Press Ctrl+C to stop the server"
echo ""

python translate_proxy.py 