from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os
import json
import logging
from datetime import datetime
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

TASK3_DIR = os.path.abspath(os.path.dirname(__file__))
MIDI_FILENAME = 'generated_music.mid'

MUSIC_STYLES = {
    'classical': {'length': 100, 'temperature': 0.8, 'style': 'classical'},
    'jazz': {'length': 80, 'temperature': 1.2, 'style': 'jazz'},
    'pop': {'length': 60, 'temperature': 0.6, 'style': 'pop'},
    'ambient': {'length': 120, 'temperature': 0.4, 'style': 'ambient'},
    'rock': {'length': 70, 'temperature': 1.0, 'style': 'rock'},
    'default': {'length': 50, 'temperature': 0.7, 'style': 'general'}
}

def validate_prompt(prompt):
    if not isinstance(prompt, str):
        return False, "Prompt must be a string"
    
    prompt = prompt.strip()
    if not prompt:
        return False, "Prompt cannot be empty"
    
    if len(prompt) > 500:
        return False, "Prompt is too long (max 500 characters)"
    
    if re.search(r'[<>{}[\]\\]', prompt):
        return False, "Prompt contains invalid characters"
    
    return True, prompt

def detect_music_style(prompt):
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ['classical', 'orchestra', 'symphony', 'piano solo']):
        return 'classical'
    elif any(word in prompt_lower for word in ['jazz', 'swing', 'blues', 'improvisation']):
        return 'jazz'
    elif any(word in prompt_lower for word in ['pop', 'popular', 'catchy', 'melody']):
        return 'pop'
    elif any(word in prompt_lower for word in ['ambient', 'atmospheric', 'calm', 'peaceful']):
        return 'ambient'
    elif any(word in prompt_lower for word in ['rock', 'guitar', 'electric', 'energetic']):
        return 'rock'
    else:
        return 'default'

@app.route('/generate_music', methods=['POST'])
def generate_music():
    try:
        if not request.is_json:
            return jsonify({
                'error': 'Invalid content type. Please send JSON with a "prompt" field.'
            }), 400
        
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        is_valid, validation_result = validate_prompt(prompt)
        if not is_valid:
            return jsonify({
                'error': f'Invalid prompt: {validation_result}'
            }), 400
        
        style = detect_music_style(prompt)
        style_params = MUSIC_STYLES[style]
        
        logger.info(f"Generating {style} music for prompt: {prompt}")
        
        try:
            result = subprocess.run(
                ['python', 'generate_and_save_midi.py', '--style', style, '--length', str(style_params['length'])],
                cwd=TASK3_DIR,
                check=True,
                capture_output=True,
                text=True
            )
        
            if result.returncode == 0:
                msg = f"🎵 Generated {style} music based on your prompt: '{prompt}'. The composition features {style_params['length']} notes with a {style} style."
                return jsonify({
                    'result': msg,
                    'midi_url': f'http://127.0.0.1:{app.config["PORT"]}/download_midi',
                    'style': style,
                    'length': style_params['length'],
                    'timestamp': datetime.utcnow().isoformat()
                })
            else:
                return jsonify({
                    'error': f"Music generation failed: {result.stderr}"
                }), 500
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Subprocess error: {e}")
            return jsonify({
                'error': f"Error generating music: {str(e)}"
            }), 500
            
    except Exception as e:
        logger.error(f"Error in generate_music endpoint: {str(e)}")
        return jsonify({
            'error': 'An unexpected error occurred. Please try again later.'
        }), 500

@app.route('/download_midi')
def download_midi():
    """Download the generated MIDI file."""
    try:
        if not os.path.exists(os.path.join(TASK3_DIR, MIDI_FILENAME)):
            return jsonify({'error': 'No music file available. Please generate music first.'}), 404
        
        return send_from_directory(TASK3_DIR, MIDI_FILENAME, as_attachment=True)
    except Exception as e:
        logger.error(f"Error downloading MIDI: {e}")
        return jsonify({'error': 'Error downloading file'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    model_exists = os.path.exists(os.path.join(TASK3_DIR, 'music_model.h5'))
    notes_exists = os.path.exists(os.path.join(TASK3_DIR, 'notes.pkl'))
    
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat(),
        'model_loaded': model_exists,
        'notes_loaded': notes_exists,
        'available_styles': list(MUSIC_STYLES.keys())
    }), 200

@app.route('/styles', methods=['GET'])
def get_styles():
    """Get available music styles."""
    return jsonify({
        'styles': MUSIC_STYLES,
        'descriptions': {
            'classical': 'Orchestral and piano compositions',
            'jazz': 'Swing and improvisational music',
            'pop': 'Catchy and melodic tunes',
            'ambient': 'Atmospheric and calming music',
            'rock': 'Energetic guitar-based music',
            'default': 'General musical composition'
        }
    }), 200

@app.route('/model_info', methods=['GET'])
def model_info():
    """Get information about the trained model."""
    try:
        model_path = os.path.join(TASK3_DIR, 'music_model.h5')
        notes_path = os.path.join(TASK3_DIR, 'notes.pkl')
        
        info = {
            'model_exists': os.path.exists(model_path),
            'notes_exists': os.path.exists(notes_path),
            'model_size': os.path.getsize(model_path) if os.path.exists(model_path) else 0
        }
        
        if os.path.exists(notes_path):
            import pickle
            with open(notes_path, 'rb') as f:
                notes = pickle.load(f)
                info['total_notes'] = len(notes)
                info['unique_notes'] = len(set(notes))
        
        return jsonify(info), 200
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        return jsonify({'error': 'Could not retrieve model information'}), 500

if __name__ == '__main__':
    print("🎵 Starting Music Generation Chatbot...")
    print("🌐 Server will run on http://localhost:5010")
    print("🏥 Health check: http://localhost:5010/health")
    print("🎼 Available styles: classical, jazz, pop, ambient, rock")
    
    app.config['PORT'] = 5010
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=True)