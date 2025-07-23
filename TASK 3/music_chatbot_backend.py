from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

TASK3_DIR = os.path.abspath(os.path.dirname(__file__))
MIDI_FILENAME = 'generated_music.mid'

@app.route('/generate_music', methods=['POST'])
def generate_music():
    data = request.get_json()
    prompt = data.get('prompt', '')
    try:
        subprocess.run(['python', 'generate_and_save_midi.py'], cwd=TASK3_DIR, check=True)
        msg = f"Music generated for prompt: '{prompt}'. Download or play below."
    except Exception as e:
        return jsonify({'result': f"Error generating music: {e}"})
    return jsonify({'result': msg, 'midi_url': 'http://127.0.0.1:5010/download_midi'})

@app.route('/download_midi')
def download_midi():
    # Always serve from TASK 3 directory
    return send_from_directory(TASK3_DIR, MIDI_FILENAME, as_attachment=True)

if __name__ == '__main__':
    app.run(port=5010, debug=True) 