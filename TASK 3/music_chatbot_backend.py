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
        # Run the music generation script
        subprocess.run(['python', 'generate_and_save_midi.py'], cwd=TASK3_DIR, check=True)
        
        msg = f"Music generated based on your prompt: '{prompt}'. You can now listen to or download the MIDI file."
        return jsonify({
            'result': msg,
            'midi_url': f'http://127.0.0.1:{app.config["PORT"]}/download_midi'
        })
    except Exception as e:
        return jsonify({'error': f"Error generating music: {str(e)}"}), 500

@app.route('/download_midi')
def download_midi():
    return send_from_directory(TASK3_DIR, MIDI_FILENAME, as_attachment=True)

if __name__ == '__main__':
    app.config['PORT'] = 5010
    app.run(port=app.config['PORT'], debug=True)