@echo off
echo Starting AI Music Generation Chatbot...
echo.
echo Step 1: Setting up dependencies...
python setup.py
echo.
echo Step 2: Starting the music generation server...
echo Server will be available at: http://localhost:5010
echo Health check: http://localhost:5010/health
echo.
echo Step 3: Open music_chatbot_frontend.html in your browser
echo.
echo Press Ctrl+C to stop the server
echo.
python music_chatbot_backend.py 