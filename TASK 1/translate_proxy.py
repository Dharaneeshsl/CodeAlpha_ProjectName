from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

LIBRETRANSLATE_URL = 'http://localhost:5001/translate'

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    if not data or not all(k in data for k in ('q', 'source', 'target')):
        return jsonify({'error': 'Missing required parameters'}), 400
    
    text = data['q']
    source = data['source']
    target = data['target']
    
    try:
        payload = {
            'q': text,
            'source': source,
            'target': target,
            'format': 'text'
        }
        res = requests.post(LIBRETRANSLATE_URL, json=payload, timeout=10)
        res.raise_for_status()
        result = res.json()
        if 'translatedText' in result:
            return jsonify({'translatedText': result['translatedText']}), 200
    except Exception as e:
        print(f"LibreTranslate failed: {e}")
    
    try:
        google_url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source}&tl={target}&dt=t&q={requests.utils.quote(text)}"
        res = requests.get(google_url, timeout=10)
        res.raise_for_status()
        data = res.json()
        
        if data and data[0] and data[0][0] and data[0][0][0]:
            return jsonify({'translatedText': data[0][0][0]}), 200
        else:
            return jsonify({'error': 'Translation failed'}), 500
    except Exception as e:
        return jsonify({'error': f'Translation service unavailable: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'translation-proxy'}), 200

if __name__ == '__main__':
    print("Starting Translation Proxy Server...")
    print("Server will run on http://localhost:5000")
    print("Health check: http://localhost:5000/health")
    app.run(port=5000, debug=True)