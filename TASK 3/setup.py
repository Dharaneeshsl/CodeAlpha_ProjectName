#!/usr/bin/env python3

import subprocess
import sys
import os

def install_requirements():
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies. Please install manually:")
        print("   pip install -r requirements.txt")
        return False
    return True

def check_model_files():
    model_files = ['music_model.h5', 'notes.pkl']
    missing_files = []
    
    for file in model_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"⚠️  Missing model files: {', '.join(missing_files)}")
        print("   The model files should be present for music generation to work.")
        print("   If you have them, please place them in the TASK 3 directory.")
        return False
    else:
        print("✅ All model files found!")
        return True

def main():
    print("🎵 AI Music Generation Chatbot Setup")
    print("=" * 45)
    
    if not install_requirements():
        return
    
    check_model_files()
    
    print("\n📋 Setup Complete!")
    print("\nTo run the application:")
    print("1. Start the backend server:")
    print("   python music_chatbot_backend.py")
    print("2. Open music_chatbot_frontend.html in your browser")
    
    print("\n✨ Features:")
    print("   - LSTM-based music composition")
    print("   - Multiple music styles (classical, jazz, pop, ambient, rock)")
    print("   - Real-time music generation")
    print("   - MIDI file download and playback")
    print("   - Modern responsive UI")
    print("   - Style detection from prompts")
    
    print("\n🎼 Available Music Styles:")
    styles = [
        "Classical - Orchestral and piano compositions",
        "Jazz - Swing and improvisational music", 
        "Pop - Catchy and melodic tunes",
        "Ambient - Atmospheric and calming music",
        "Rock - Energetic guitar-based music"
    ]
    for style in styles:
        print(f"   - {style}")
    
    print("\n🔧 API Endpoints:")
    print("   - POST /generate_music - Generate music from prompt")
    print("   - GET /download_midi - Download generated MIDI file")
    print("   - GET /health - Health check")
    print("   - GET /styles - Get available music styles")
    print("   - GET /model_info - Get model information")
    
    print("\n🌐 Server will run on: http://localhost:5010")
    print("🏥 Health check: http://localhost:5010/health")

if __name__ == "__main__":
    main() 