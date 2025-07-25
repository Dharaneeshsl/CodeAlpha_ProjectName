# CodeAlpha Internship Projects

This repository contains three complete web applications developed as part of the CodeAlpha internship program.

## Project Overview

### TASK 1 - Language Translation Tool
A modern web-based translation tool with support for multiple languages.

**Features:**
- Clean, responsive UI with modern design
- Support for 10+ languages (English, Spanish, French, German, Hindi, Chinese, Arabic, Russian, Japanese, Korean)
- Real-time translation using Google Translate API
- Flask proxy backend for LibreTranslate integration
- Error handling and user feedback

**Files:**
- `language_translation_tool.html` - Frontend interface
- `translate_proxy.py` - Flask backend proxy

**Usage:**
1. Open `language_translation_tool.html` in a web browser
2. Select source and target languages
3. Enter text and click "Translate"

### TASK 2 - FAQ Chatbot
An intelligent FAQ chatbot that combines rule-based matching with GPT-3.5 integration.

**Features:**
- Hybrid approach: TF-IDF matching + GPT-3.5 fallback
- Modern chat interface with loading indicators
- Rate limiting and input validation
- Health check endpoints
- Comprehensive error handling

**Files:**
- `faq_chatbot_gpt.py` - Main backend with GPT integration
- `faq_chatbot_api.py` - Basic FAQ backend
- `faq_chatbot_frontend.html` - Chat interface
- `faq_data.json` - FAQ database
- `requirements.txt` - Dependencies
- `README.md` - Detailed documentation

**Setup:**
1. Install dependencies: `pip install -r requirements.txt`
2. Add OpenAI API key to `.env` file
3. Run: `python faq_chatbot_gpt.py`
4. Open `faq_chatbot_frontend.html`

### TASK 3 - Music Generation Chatbot
An AI-powered music generation system using LSTM neural networks.

**Features:**
- LSTM-based music composition
- Chat interface for music prompts
- MIDI file generation and download
- Pre-trained model for instant generation
- Audio playback capabilities

**Files:**
- `music_chatbot_backend.py` - Flask API server
- `music_chatbot_frontend.html` - Chat interface
- `train_lstm_model.py` - Model training script
- `generate_and_save_midi.py` - Music generation
- `music_model.h5` - Pre-trained LSTM model
- `notes.pkl` - Processed musical notes

**Usage:**
1. Run: `python music_chatbot_backend.py`
2. Open `music_chatbot_frontend.html`
3. Enter music prompts and generate compositions

## Technologies Used

- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Backend:** Python, Flask, CORS
- **AI/ML:** OpenAI GPT-3.5, TensorFlow/Keras, NLTK
- **Music:** Music21, MIDI processing
- **Data:** JSON, Pickle

## Installation

1. Clone the repository
2. Navigate to each task directory
3. Install Python dependencies as needed
4. Configure API keys where required
5. Run the applications

## License

MIT License - See individual task directories for specific licensing information.

## Author

Developed as part of CodeAlpha internship program.
