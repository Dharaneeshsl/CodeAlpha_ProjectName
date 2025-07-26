# TASK 4 - Object Detection and Tracking

A comprehensive real-time object detection and tracking system using OpenCV, YOLO, and computer vision techniques. The system can detect and track objects in live video streams from webcams or video files, with both command-line and web interfaces.

## 🎯 Features

- **Real-time Object Detection**: Using YOLO (You Only Look Once) model
- **Object Tracking**: Unique tracking IDs for each detected object
- **Multiple Input Sources**: Webcam, video files, and external cameras
- **Dual Interface**: Command-line and web-based interfaces
- **Live Video Streaming**: Real-time video feed with detection overlays
- **Fallback Detection**: Face detection when YOLO model is unavailable
- **Configurable Parameters**: Adjustable confidence and NMS thresholds
- **Frame Capture**: Save individual frames with detections
- **Statistics Dashboard**: Live FPS, object count, and performance metrics

## 📋 Requirements Met

✅ **Set up real-time video input using a webcam or video file (OpenCV)**  
✅ **Use a pre-trained model like YOLO or Faster R-CNN for object detection**  
✅ **Process each video frame to detect objects and draw bounding boxes**  
✅ **Apply object tracking using algorithms like SORT or Deep SORT**  
✅ **Display the output with labels and tracking IDs in real time**  

## 📁 Files

- `object_detection_tracking.py` - Main CLI application with YOLO detection
- `web_interface.py` - Flask web server with real-time streaming
- `templates/index.html` - Modern web interface with controls
- `requirements.txt` - Python dependencies
- `setup.py` - Automated setup and dependency installation
- `run_detection.bat` - Windows execution script
- `run_detection.sh` - Unix/Linux execution script

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Windows
run_detection.bat

# Unix/Linux
./run_detection.sh
```

### Option 2: Manual Setup
1. Install dependencies:
   ```bash
   python setup.py
   ```

2. Run the application:
   ```bash
   # CLI with webcam
   python object_detection_tracking.py --source 0
   
   # CLI with video file
   python object_detection_tracking.py --source video.mp4
   
   # Web interface
   python web_interface.py
   ```

## 🎮 Usage

### Command Line Interface

#### Basic Usage
```bash
# Use webcam
python object_detection_tracking.py --source 0

# Use video file
python object_detection_tracking.py --source path/to/video.mp4

# Save output video
python object_detection_tracking.py --source 0 --output output.mp4
```

#### Advanced Options
```bash
# Adjust detection confidence
python object_detection_tracking.py --source 0 --confidence 0.7

# Adjust NMS threshold
python object_detection_tracking.py --source 0 --nms 0.3

# Use custom YOLO model
python object_detection_tracking.py --source 0 --model /path/to/model
```

#### Controls
- **'q'** - Quit the application
- **'s'** - Save current frame

### Web Interface

1. Start the web server:
   ```bash
   python web_interface.py
   ```

2. Open your browser and go to: `http://localhost:5020`

3. Configure settings and click "Start Detection"

#### Web Interface Features
- **Real-time Video Streaming**: Live video feed with detection overlays
- **Camera Selection**: Choose from multiple camera sources
- **Parameter Adjustment**: Sliders for confidence and NMS thresholds
- **Live Statistics**: FPS, object count, and performance metrics
- **Frame Capture**: Save individual frames with detections
- **Start/Stop Controls**: Easy control over detection process

## 🔧 Technical Architecture

### Object Detection
- **YOLO Model**: Pre-trained YOLOv4 for object detection
- **Fallback Mode**: OpenCV face detection when YOLO unavailable
- **COCO Classes**: 80+ object classes supported
- **Confidence Filtering**: Configurable detection thresholds
- **Non-Maximum Suppression**: Eliminate duplicate detections

### Object Tracking
- **Simple Tracking Algorithm**: Distance-based object association
- **Unique IDs**: Persistent tracking IDs for each object
- **Track History**: Visual trails showing object movement
- **Timeout Management**: Automatic track cleanup
- **Multi-Object Support**: Track multiple objects simultaneously

### Video Processing
- **OpenCV Integration**: Efficient video capture and processing
- **Real-time Performance**: Optimized for live streaming
- **Multiple Formats**: Support for various video codecs
- **Frame Rate Control**: Configurable processing speed
- **Memory Management**: Efficient frame handling

### Web Interface
- **Flask Backend**: Lightweight web server
- **Real-time Streaming**: MJPEG video streaming
- **RESTful API**: JSON-based communication
- **Threading**: Non-blocking video processing
- **Cross-platform**: Works on all modern browsers

## 🎨 Detection Features

### Supported Objects
The system can detect 80+ object classes including:
- **People**: person
- **Vehicles**: car, truck, bus, motorcycle, bicycle
- **Animals**: dog, cat, horse, bird, etc.
- **Objects**: chair, table, laptop, phone, etc.
- **Food**: apple, banana, pizza, etc.

### Detection Output
- **Bounding Boxes**: Colored rectangles around detected objects
- **Labels**: Object class names with confidence scores
- **Tracking IDs**: Unique identifiers for each tracked object
- **Trails**: Visual paths showing object movement
- **Statistics**: Real-time performance metrics

### Performance Metrics
- **FPS**: Frames per second processing rate
- **Object Count**: Number of detected objects
- **Active Tracks**: Currently tracked objects
- **Frame Count**: Total frames processed
- **Detection Confidence**: Average confidence scores

## 🔧 Configuration

### Detection Parameters
```python
# Confidence threshold (0.1 - 1.0)
confidence_threshold = 0.5

# Non-maximum suppression threshold (0.1 - 1.0)
nms_threshold = 0.4

# Maximum tracking distance
max_tracking_distance = 100

# Track timeout (seconds)
track_timeout = 2.0
```

### Video Settings
```python
# Input resolution
input_width = 640
input_height = 480

# Processing resolution
process_width = 416
process_height = 416

# Output frame rate
target_fps = 30
```

## 🚨 Troubleshooting

### Common Issues

1. **Camera Not Found**
   - Check camera permissions
   - Try different camera indices (0, 1, 2)
   - Ensure camera is not in use by other applications

2. **YOLO Model Not Found**
   - Download YOLOv4 files from official repository
   - Use fallback face detection mode
   - Check file paths and permissions

3. **Low Performance**
   - Reduce input resolution
   - Increase confidence threshold
   - Use GPU acceleration if available
   - Close other resource-intensive applications

4. **Web Interface Not Loading**
   - Check if port 5020 is available
   - Ensure firewall allows the connection
   - Try different browser

### Performance Tips
- **GPU Acceleration**: Install OpenCV with CUDA support
- **Resolution**: Lower input resolution for better performance
- **Confidence**: Higher confidence threshold reduces false positives
- **NMS**: Lower NMS threshold for fewer duplicate detections

## 📊 API Endpoints

### Web Interface API
- `GET /` - Main web interface
- `GET /video_feed` - Real-time video stream
- `POST /start_detection` - Start object detection
- `POST /stop_detection` - Stop object detection
- `GET /get_stats` - Get detection statistics
- `POST /save_frame` - Save current frame
- `GET /health` - Health check

### Example API Usage
```bash
# Start detection
curl -X POST http://localhost:5020/start_detection \
  -H "Content-Type: application/json" \
  -d '{"source": 0, "confidence": 0.5, "nms": 0.4}'

# Get statistics
curl http://localhost:5020/get_stats

# Save frame
curl -X POST http://localhost:5020/save_frame
```

## 🎯 Example Use Cases

### Security and Surveillance
- Monitor entrances and exits
- Track people movement
- Detect unauthorized access
- Count visitors

### Traffic Analysis
- Count vehicles
- Track traffic flow
- Monitor parking lots
- Analyze pedestrian movement

### Retail Analytics
- Customer counting
- Queue monitoring
- Product interaction tracking
- Store traffic analysis

### Industrial Applications
- Quality control inspection
- Equipment monitoring
- Safety compliance
- Process automation

## 📄 License

MIT License - See LICENSE file for details.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 🎯 Acknowledgments

- **OpenCV**: Computer vision library
- **YOLO**: Real-time object detection
- **COCO Dataset**: Object detection training data
- **Flask**: Web framework
- **Computer Vision Community**: Research and development 