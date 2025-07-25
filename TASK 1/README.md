# TASK 1 - Language Translation Tool

A modern, responsive web-based translation tool that supports multiple languages with a clean user interface.

## Features

- **Multi-language Support**: Translate between 10+ languages including English, Spanish, French, German, Hindi, Chinese, Arabic, Russian, Japanese, and Korean
- **Modern UI**: Clean, responsive design with gradient styling and smooth transitions
- **Real-time Translation**: Instant translation using Google Translate API
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Cross-platform**: Works on desktop and mobile browsers

## Files

- `language_translation_tool.html` - Complete frontend application with embedded CSS and JavaScript
- `translate_proxy.py` - Flask backend proxy server for LibreTranslate integration

## Usage

### Option 1: Direct Browser Usage (Recommended)
1. Open `language_translation_tool.html` in any modern web browser
2. Select your source language from the dropdown
3. Select your target language from the dropdown
4. Enter the text you want to translate
5. Click the "Translate" button
6. View the translated text in the result area

### Option 2: With Backend Proxy
1. Install Flask and dependencies:
   ```bash
   pip install flask flask-cors requests
   ```
2. Start the proxy server:
   ```bash
   python translate_proxy.py
   ```
3. The proxy will run on `http://localhost:5000`
4. Modify the frontend to use the proxy endpoint if needed

## Technical Details

### Frontend (`language_translation_tool.html`)
- **HTML5** structure with semantic elements
- **CSS3** with modern styling, gradients, and responsive design
- **JavaScript ES6+** with async/await for API calls
- Uses Google Translate's unofficial API endpoint
- Responsive design that works on mobile devices

### Backend (`translate_proxy.py`)
- **Flask** web server with CORS support
- Proxy endpoint for LibreTranslate integration
- Error handling and JSON response formatting
- Runs on port 5000 by default

## Supported Languages

| Code | Language |
|------|----------|
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

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Notes

- The frontend uses Google Translate's unofficial API which may have rate limits
- For production use, consider using official translation APIs
- The proxy server is optional and can be used for additional processing or caching
- No API keys required for basic functionality

## License

MIT License
