# TASK 1 - Language Translation Tool

A modern, responsive web-based translation tool that supports multiple languages with a clean user interface and advanced features.

## ✨ Features

- **Multi-language Support**: Translate between 10+ languages including English, Spanish, French, German, Hindi, Chinese, Arabic, Russian, Japanese, and Korean
- **Auto-language Detection**: Automatically detect the source language of your text
- **Modern UI**: Clean, responsive design with gradient styling, smooth transitions, and loading animations
- **Real-time Translation**: Instant translation using Google Translate API with fallback support
- **Enhanced Error Handling**: Comprehensive error handling with user-friendly messages and visual feedback
- **Cross-platform**: Works on desktop and mobile browsers
- **Keyboard Shortcuts**: Use Ctrl+Enter to translate quickly
- **Loading States**: Visual feedback during translation with spinner animations

## 📁 Files

- `language_translation_tool.html` - Complete frontend application with embedded CSS and JavaScript
- `translate_proxy.py` - Enhanced Flask backend proxy server with fallback support
- `requirements.txt` - Python dependencies
- `setup.py` - Automated setup script
- `run_translator.bat` - Windows batch file for easy execution
- `run_translator.sh` - Unix/Linux shell script for easy execution

## 🚀 Quick Start

### Option 1: Direct Browser Usage (Recommended)
1. Open `language_translation_tool.html` in any modern web browser
2. Select your source language (or use "Auto-detect")
3. Select your target language
4. Enter the text you want to translate
5. Click the "Translate" button or press Ctrl+Enter
6. View the translated text in the result area

### Option 2: With Backend Proxy
1. Run the setup script:
   ```bash
   python setup.py
   ```
2. Start the proxy server:
   ```bash
   python translate_proxy.py
   ```
3. The server will run on `http://localhost:5000`
4. Health check available at `http://localhost:5000/health`

### Option 3: Using Scripts
- **Windows**: Double-click `run_translator.bat`
- **Unix/Linux**: Run `./run_translator.sh`

## 🔧 Technical Details

### Frontend (`language_translation_tool.html`)
- **HTML5** structure with semantic elements
- **CSS3** with modern styling, gradients, responsive design, and animations
- **JavaScript ES6+** with async/await for API calls
- **Auto-language detection** with debounced input handling
- **Loading animations** and visual feedback
- **Error handling** with color-coded messages
- **Keyboard shortcuts** for enhanced UX

### Backend (`translate_proxy.py`)
- **Flask** web server with CORS support
- **Dual translation service** support (LibreTranslate + Google Translate fallback)
- **Enhanced error handling** with timeout management
- **Health check endpoint** for monitoring
- **JSON response formatting** with proper error codes
- Runs on port 5000 by default

## 🌐 Supported Languages

| Code | Language |
|------|----------|
| auto | Auto-detect |
| en   | English  |
| es   | Spanish  |
| fr   | French   |
| de   | German   |
| hi   | Hindi    |
| zh   | Chinese  |
| ar   | Arabic   |
| ru   | Russian  |
| ja   | Japanese |
| ko   | Korean   |

## 🎨 UI Features

- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Modern Styling**: Gradient buttons, smooth transitions, and clean typography
- **Loading Animations**: Spinner animation during translation
- **Color-coded Feedback**: Green for success, red for errors
- **Auto-resize Textarea**: Adapts to content length
- **Keyboard Navigation**: Full keyboard support

## 🔒 Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 📝 Usage Tips

1. **Auto-detect**: Use the "Auto-detect" option to automatically identify the source language
2. **Keyboard Shortcuts**: Press Ctrl+Enter to translate quickly
3. **Long Text**: The tool handles long paragraphs and documents
4. **Multiple Languages**: Switch between languages seamlessly
5. **Error Recovery**: If translation fails, try again or check your internet connection

## 🔧 Advanced Configuration

### Backend Configuration
The Flask server can be configured by modifying `translate_proxy.py`:
- Change port number in the `app.run()` call
- Modify timeout values for API calls
- Add additional translation services

### Frontend Customization
The HTML file can be customized:
- Modify CSS variables for different color schemes
- Add more languages to the dropdown
- Customize animations and transitions

## 🚨 Notes

- The frontend uses Google Translate's unofficial API which may have rate limits
- For production use, consider using official translation APIs with proper authentication
- The proxy server provides fallback support and can be extended for caching
- No API keys required for basic functionality
- LibreTranslate integration requires a running LibreTranslate instance

## 📄 License

MIT License

## 🤝 Contributing

Feel free to submit issues and enhancement requests!
