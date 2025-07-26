#!/usr/bin/env python3

import subprocess
import sys
import os
import urllib.request
import zipfile

def install_requirements():
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies. Please install manually:")
        print("   pip install -r requirements.txt")
        return False

def download_yolo_model():
    model_files = ['yolov4.cfg', 'yolov4.weights', 'coco.names']
    
    print("Checking YOLO model files...")
    
    for file in model_files:
        if not os.path.exists(file):
            print(f"⚠️  Missing {file}")
    
    print("\nTo use YOLO model:")
    print("1. Download YOLOv4 files from: https://github.com/AlexeyAB/darknet")
    print("2. Place yolov4.cfg, yolov4.weights, and coco.names in this directory")
    print("3. Or use the fallback face detection mode")
    
    return True

def check_opencv():
    try:
        import cv2
        print(f"✅ OpenCV version: {cv2.__version__}")
        return True
    except ImportError:
        print("❌ OpenCV not found. Please install opencv-python")
        return False

def main():
    print("🎯 Object Detection and Tracking System Setup")
    print("=" * 50)
    
    if not install_requirements():
        return
    
    if not check_opencv():
        return
    
    download_yolo_model()
    
    print("\n📋 Setup Complete!")
    print("\nTo run the application:")
    print("\nOption 1: Command Line Interface")
    print("   python object_detection_tracking.py --source 0")
    print("   python object_detection_tracking.py --source video.mp4")
    
    print("\nOption 2: Web Interface")
    print("   python web_interface.py")
    print("   Then open http://localhost:5020 in your browser")
    
    print("\n✨ Features:")
    print("   - Real-time object detection using YOLO")
    print("   - Object tracking with unique IDs")
    print("   - Webcam and video file support")
    print("   - Web interface with live streaming")
    print("   - Fallback face detection mode")
    print("   - Configurable confidence and NMS thresholds")
    
    print("\n🎮 Controls:")
    print("   - Press 'q' to quit (CLI mode)")
    print("   - Press 's' to save current frame")
    print("   - Web interface has start/stop buttons")
    
    print("\n🔧 Command Line Options:")
    print("   --source: Video source (0=webcam, or file path)")
    print("   --output: Output video path (optional)")
    print("   --confidence: Detection confidence threshold (0.1-1.0)")
    print("   --nms: Non-maximum suppression threshold (0.1-1.0)")
    
    print("\n🌐 Web Interface:")
    print("   - Real-time video streaming")
    print("   - Live statistics and controls")
    print("   - Frame capture functionality")
    print("   - Multiple camera support")
    
    print("\n📁 Files:")
    print("   - object_detection_tracking.py: Main CLI application")
    print("   - web_interface.py: Flask web server")
    print("   - templates/index.html: Web interface")
    print("   - requirements.txt: Python dependencies")

if __name__ == "__main__":
    main() 