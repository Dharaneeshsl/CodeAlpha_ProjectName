#!/usr/bin/env python3

from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import threading
import time
import os
import json
from datetime import datetime
import logging

from object_detection_tracking import ObjectTracker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

camera = None
output_frame = None
lock = threading.Lock()
tracker = None
is_processing = False
detection_stats = {
    'total_objects': 0,
    'current_objects': 0,
    'fps': 0,
    'frame_count': 0
}

def initialize_camera(source=0):
    global camera
    try:
        if isinstance(source, str) and source.isdigit():
            source = int(source)
        camera = cv2.VideoCapture(source)
        if not camera.isOpened():
            logger.error("Failed to open camera")
            return False
        logger.info(f"Camera initialized with source: {source}")
        return True
    except Exception as e:
        logger.error(f"Error initializing camera: {e}")
        return False

def process_frames():
    global output_frame, tracker, is_processing, detection_stats
    
    if not camera:
        return
    
    frame_count = 0
    start_time = time.time()
    
    while is_processing:
        ret, frame = camera.read()
        if not ret:
            break
        
        frame_count += 1
        
        detections = tracker.detect_objects(frame)
        
        tracks = tracker.update_tracking(detections)
        
        frame = tracker.draw_detections(frame, tracks)
        
        elapsed_time = time.time() - start_time
        current_fps = frame_count / elapsed_time if elapsed_time > 0 else 0
        
        detection_stats.update({
            'total_objects': len(tracks),
            'current_objects': len([t for t in tracks.values() if t['active']]),
            'fps': current_fps,
            'frame_count': frame_count
        })
        
        info_text = f"FPS: {current_fps:.1f} | Objects: {len(tracks)}"
        cv2.putText(frame, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp, (10, frame.shape[0] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Update output frame
        with lock:
            output_frame = frame.copy()
        
        # Control frame rate
        time.sleep(0.03)  # ~30 FPS

def generate_frames():
    """Generate video frames for streaming"""
    global output_frame
    
    while True:
        with lock:
            if output_frame is None:
                continue
            
            # Encode frame
            (flag, encoded_image) = cv2.imencode(".jpg", output_frame)
            if not flag:
                continue
        
        # Yield frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + encoded_image.tobytes() + b'\r\n')

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_detection', methods=['POST'])
def start_detection():
    """Start object detection and tracking"""
    global tracker, is_processing
    
    try:
        data = request.get_json()
        source = data.get('source', 0)
        confidence = data.get('confidence', 0.5)
        nms = data.get('nms', 0.4)
        
        # Initialize camera
        if not initialize_camera(source):
            return jsonify({'error': 'Failed to initialize camera'}), 500
        
        # Initialize tracker
        tracker = ObjectTracker(
            confidence_threshold=confidence,
            nms_threshold=nms
        )
        
        # Start processing
        is_processing = True
        processing_thread = threading.Thread(target=process_frames)
        processing_thread.daemon = True
        processing_thread.start()
        
        logger.info("Object detection started")
        return jsonify({'status': 'success', 'message': 'Detection started'})
    
    except Exception as e:
        logger.error(f"Error starting detection: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/stop_detection', methods=['POST'])
def stop_detection():
    """Stop object detection and tracking"""
    global is_processing, camera
    
    try:
        is_processing = False
        if camera:
            camera.release()
        
        logger.info("Object detection stopped")
        return jsonify({'status': 'success', 'message': 'Detection stopped'})
    
    except Exception as e:
        logger.error(f"Error stopping detection: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/get_stats')
def get_stats():
    """Get current detection statistics"""
    return jsonify(detection_stats)

@app.route('/save_frame', methods=['POST'])
def save_frame():
    """Save current frame"""
    global output_frame
    
    try:
        if output_frame is None:
            return jsonify({'error': 'No frame available'}), 400
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"frame_{timestamp}.jpg"
        
        cv2.imwrite(filename, output_frame)
        
        logger.info(f"Frame saved as {filename}")
        return jsonify({'status': 'success', 'filename': filename})
    
    except Exception as e:
        logger.error(f"Error saving frame: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'is_processing': is_processing,
        'camera_initialized': camera is not None and camera.isOpened() if camera else False
    })

if __name__ == '__main__':
    print("🌐 Object Detection Web Interface")
    print("=" * 40)
    print("Server will run on http://localhost:5020")
    print("Health check: http://localhost:5020/health")
    print("=" * 40)
    
    app.run(host='0.0.0.0', port=5020, debug=True, threaded=True) 