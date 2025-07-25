from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

LIBRETRANSLATE_URL = 'http://localhost:5001/translate'

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    if not data or not all(k in data for k in ('q', 'source', 'target')):
        return jsonify({'error': 'Missing required parameters'}), 400
    payload = {
        'q': data['q'],
        'source': data['source'],
        'target': data['target'],
        'format': 'text'
    }
    try:
        res = requests.post(LIBRETRANSLATE_URL, json=payload)
        res.raise_for_status()
        return jsonify(res.json()), res.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)