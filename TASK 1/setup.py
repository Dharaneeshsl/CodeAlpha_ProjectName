#!/usr/bin/env python3
"""
Setup script for Language Translation Tool
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required Python packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies. Please install manually:")
        print("   pip install -r requirements.txt")
        return False
    return True

def main():
    print("🚀 Language Translation Tool Setup")
    print("=" * 40)
    
    # Install dependencies
    if not install_requirements():
        return
    
    print("\n📋 Setup Complete!")
    print("\nTo run the application:")
    print("1. For frontend only (recommended):")
    print("   - Open 'language_translation_tool.html' in your web browser")
    print("   - No additional setup required")
    
    print("\n2. With backend proxy:")
    print("   - Run: python translate_proxy.py")
    print("   - Server will start on http://localhost:5000")
    print("   - Health check: http://localhost:5000/health")
    
    print("\n✨ Features:")
    print("   - Multi-language support (10+ languages)")
    print("   - Auto-language detection")
    print("   - Modern responsive UI")
    print("   - Real-time translation")
    print("   - Error handling and loading states")
    
    print("\n🌐 Supported Languages:")
    languages = [
        "English (en)", "Spanish (es)", "French (fr)", "German (de)",
        "Hindi (hi)", "Chinese (zh)", "Arabic (ar)", "Russian (ru)",
        "Japanese (ja)", "Korean (ko)"
    ]
    for lang in languages:
        print(f"   - {lang}")

if __name__ == "__main__":
    main() 