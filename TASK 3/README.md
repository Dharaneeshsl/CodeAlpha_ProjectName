# TASK 3 - AI Music Generation Chatbot

An intelligent music generation system that uses LSTM neural networks to compose original music based on user prompts. The system can generate music in multiple styles and provides both MIDI download and audio playback capabilities.

## 🎵 Features

- **LSTM-based Music Composition**: Advanced neural network model trained on MIDI data
- **Multiple Music Styles**: Classical, Jazz, Pop, Ambient, Rock, and more
- **Smart Style Detection**: Automatically detects music style from user prompts
- **Real-time Generation**: Instant music composition with customizable parameters
- **MIDI Export**: Download generated music as MIDI files
- **Audio Playback**: Built-in audio player for immediate listening
- **Modern UI**: Beautiful, responsive chat interface with music controls
- **Style Indicators**: Visual indicators showing the detected music style
- **Quick Suggestions**: Pre-built prompts for different music styles

## 🎼 Supported Music Styles

| Style | Description | Characteristics |
|-------|-------------|-----------------|
| **Classical** | Orchestral and piano compositions | Structured, melodic, traditional |
| **Jazz** | Swing and improvisational music | Complex chords, syncopated rhythms |
| **Pop** | Catchy and melodic tunes | Simple harmonies, memorable melodies |
| **Ambient** | Atmospheric and calming music | Slow tempo, atmospheric sounds |
| **Rock** | Energetic guitar-based music | Fast tempo, power chords |
| **Default** | General musical composition | Balanced, versatile |

## 📁 Files

- `music_chatbot_backend.py` - Enhanced Flask backend with style detection
- `music_chatbot_frontend.html` - Modern responsive chat interface
- `generate_and_save_midi.py` - Enhanced music generation with style support
- `train_lstm_model.py` - LSTM model training script
- `preprocess_midi.py` - MIDI data preprocessing
- `music_model.h5` - Pre-trained LSTM model
- `notes.pkl` - Processed musical notes data
- `requirements.txt` - Python dependencies
- `setup.py` - Automated setup script
- `run_music.bat` - Windows execution script
- `run_music.sh` - Unix/Linux execution script

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Windows
run_music.bat

# Unix/Linux
./run_music.sh
```

### Option 2: Manual Setup
1. Install dependencies:
   ```bash
   python setup.py
   ```

2. Start the backend server:
   ```bash
   python music_chatbot_backend.py
   ```

3. Open `music_chatbot_frontend.html` in your web browser

## 🎯 Usage

### Basic Music Generation
1. Open the chat interface
2. Type a music prompt (e.g., "peaceful classical piano piece")
3. Click "Generate" or press Enter
4. Wait for the AI to compose your music
5. Listen to the result and download the MIDI file

### Style-Specific Prompts
- **Classical**: "Create a peaceful classical piano piece"
- **Jazz**: "Generate an upbeat jazz composition"
- **Pop**: "Make a catchy pop melody"
- **Ambient**: "Create calming ambient music"
- **Rock**: "Generate energetic rock music"

### Advanced Features
- **Style Detection**: The system automatically detects the music style from your prompt
- **Custom Parameters**: Different styles use different generation parameters
- **Real-time Feedback**: See the detected style and generation progress
- **Multiple Downloads**: Generate and download multiple compositions

## 🔧 API Endpoints

### Generate Music
- **POST** `/generate_music`
- **Body**: `{"prompt": "your music description"}`
- **Response**: Music generation result with download link

### Download MIDI
- **GET** `/download_midi`
- **Response**: MIDI file download

### Health Check
- **GET** `/health`
- **Response**: Server status and model information

### Get Styles
- **GET** `/styles`
- **Response**: Available music styles and descriptions

### Model Info
- **GET** `/model_info`
- **Response**: Detailed model information

## 🎨 Technical Architecture

### Backend (Python/Flask)
- **Flask**: Web framework for API endpoints
- **TensorFlow/Keras**: LSTM neural network for music generation
- **Music21**: MIDI processing and music analysis
- **Style Detection**: NLP-based prompt analysis
- **Error Handling**: Comprehensive error management

### Frontend (HTML/CSS/JavaScript)
- **Modern Design**: Glassmorphism UI with gradients
- **Responsive Layout**: Works on all device sizes
- **Real-time Chat**: Live music generation interface
- **Audio Controls**: Built-in MIDI playback
- **Style Indicators**: Visual style classification

### AI Model
- **LSTM Architecture**: Long Short-Term Memory neural network
- **Sequence Learning**: Trained on MIDI note sequences
- **Style Adaptation**: Different parameters for each music style
- **Temperature Control**: Adjustable creativity levels

## 🎼 Music Generation Process

1. **Prompt Analysis**: Parse user input for style detection
2. **Model Loading**: Load pre-trained LSTM model
3. **Sequence Generation**: Generate note sequences based on style
4. **MIDI Creation**: Convert notes to MIDI format
5. **Instrument Selection**: Choose appropriate instruments
6. **File Output**: Save as downloadable MIDI file

## 📊 Model Information

- **Architecture**: LSTM with dropout layers
- **Training Data**: MIDI files from various genres
- **Sequence Length**: 20 notes for context
- **Vocabulary Size**: Based on unique notes/chords
- **Model Size**: ~2.4MB (compressed)

## 🎵 Music Features

### Generated Music Characteristics
- **Length**: 50-120 notes depending on style
- **Tempo**: Style-appropriate timing
- **Instruments**: Piano, Guitar, Synth based on style
- **Complexity**: Varies by genre (simple pop to complex jazz)

### MIDI File Format
- **Format**: Standard MIDI (.mid)
- **Compatibility**: Works with all music software
- **Quality**: Professional-grade output
- **Size**: Compact file sizes

## 🔧 Configuration

### Style Parameters
```python
MUSIC_STYLES = {
    'classical': {'length': 100, 'temperature': 0.8},
    'jazz': {'length': 80, 'temperature': 1.2},
    'pop': {'length': 60, 'temperature': 0.6},
    'ambient': {'length': 120, 'temperature': 0.4},
    'rock': {'length': 70, 'temperature': 1.0}
}
```

### Model Settings
- **Sequence Length**: 20 notes
- **Temperature Range**: 0.1-2.0
- **Generation Length**: 50-120 notes
- **Dropout Rate**: 0.3

## 🚨 Troubleshooting

### Common Issues
1. **Model Not Found**: Ensure `music_model.h5` and `notes.pkl` are present
2. **Dependencies**: Run `python setup.py` to install requirements
3. **Port Conflicts**: Change port in `music_chatbot_backend.py`
4. **MIDI Playback**: Use compatible browser/audio player

### Performance Tips
- **GPU Acceleration**: Install TensorFlow-GPU for faster generation
- **Memory**: Ensure sufficient RAM for model loading
- **Network**: Stable connection for real-time generation

## 🎉 Example Prompts

### Classical
- "Create a peaceful classical piano piece"
- "Generate a dramatic orchestral composition"
- "Make a gentle symphony movement"

### Jazz
- "Generate an upbeat jazz composition"
- "Create a smooth jazz piano solo"
- "Make a swing jazz piece"

### Pop
- "Create a catchy pop melody"
- "Generate an upbeat pop song"
- "Make a romantic pop ballad"

### Ambient
- "Create calming ambient music"
- "Generate atmospheric background music"
- "Make peaceful meditation music"

### Rock
- "Generate energetic rock music"
- "Create a powerful guitar riff"
- "Make an upbeat rock anthem"

## 📄 License

MIT License - See LICENSE file for details.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 🎵 Acknowledgments

- **Music21**: MIDI processing library
- **TensorFlow/Keras**: Neural network framework
- **LSTM Architecture**: For sequence learning
- **MIDI Format**: Standard music file format 