#!/bin/bash

echo "🎵 AI Music Generation Chatbot"
echo "=============================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    exit 1
fi

# Setup dependencies
echo "📦 Setting up dependencies..."
python3 setup.py

echo ""
echo "🎼 Starting Music Generation server..."
echo "Server will be available at: http://localhost:5010"
echo "Health check: http://localhost:5010/health"
echo ""
echo "📱 Open music_chatbot_frontend.html in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python3 music_chatbot_backend.py 