#!/bin/bash

echo "🎯 Object Detection and Tracking System"
echo "========================================"
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
echo "🎮 Choose your interface:"
echo ""
echo "1. Command Line Interface (CLI) - Webcam"
echo "2. Command Line Interface (CLI) - Video File"
echo "3. Web Interface"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "📹 Starting CLI with webcam..."
        python3 object_detection_tracking.py --source 0
        ;;
    2)
        echo ""
        read -p "Enter video file path: " video
        echo "📹 Starting CLI with video file..."
        python3 object_detection_tracking.py --source "$video"
        ;;
    3)
        echo ""
        echo "🌐 Starting web interface..."
        echo "Server will be available at: http://localhost:5020"
        echo ""
        python3 web_interface.py
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac 