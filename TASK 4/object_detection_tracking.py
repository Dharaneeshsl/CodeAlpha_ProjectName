#!/usr/bin/env python3

import cv2
import numpy as np
import argparse
import time
import os
import sys
from collections import deque
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ObjectTracker:
    def __init__(self, model_path=None, confidence_threshold=0.5, nms_threshold=0.4):
        self.confidence_threshold = confidence_threshold
        self.nms_threshold = nms_threshold
        self.trackers = {}
        self.track_id = 0
        self.track_history = {}
        self.max_history = 30
        
        self.load_yolo_model(model_path)
        
        self.class_names = self.load_class_names()
        
        self.colors = np.random.uniform(0, 255, size=(len(self.class_names), 3))
        
        logger.info("Object Detection and Tracking system initialized")
    
    def load_yolo_model(self, model_path):
        try:
            if model_path and os.path.exists(model_path):
                self.net = cv2.dnn.readNetFromDarknet(
                    os.path.join(model_path, "yolov4.cfg"),
                    os.path.join(model_path, "yolov4.weights")
                )
                logger.info(f"Loaded custom YOLO model from {model_path}")
            else:
                self.net = cv2.dnn.readNetFromDarknet(
                    "yolov4.cfg",
                    "yolov4.weights"
                )
                logger.info("Loaded OpenCV YOLO model")
            
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
            
        except Exception as e:
            logger.error(f"Error loading YOLO model: {e}")
            logger.info("Falling back to OpenCV's DNN face detector")
            self.use_face_detector = True
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        else:
            self.use_face_detector = False
    
    def load_class_names(self):
        try:
            with open("coco.names", "r") as f:
                return [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            return [
                'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
                'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat',
                'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
                'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
                'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
                'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
                'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop',
                'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
                'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
            ]
    
    def get_output_layers(self):
        layer_names = self.net.getLayerNames()
        try:
            return [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        except:
            return [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
    
    def detect_objects(self, frame):
        """Detect objects in the frame using YOLO"""
        if self.use_face_detector:
            return self.detect_faces(frame)
        
        height, width = frame.shape[:2]
        
        # Create blob from image
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        
        # Forward pass
        outputs = self.net.forward(self.get_output_layers())
        
        # Process detections
        boxes = []
        confidences = []
        class_ids = []
        
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                if confidence > self.confidence_threshold:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        
        # Apply non-maximum suppression
        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence_threshold, self.nms_threshold)
        
        detections = []
        if len(indices) > 0:
            for i in indices.flatten():
                x, y, w, h = boxes[i]
                detections.append({
                    'bbox': [x, y, w, h],
                    'confidence': confidences[i],
                    'class_id': class_ids[i],
                    'class_name': self.class_names[class_ids[i]]
                })
        
        return detections
    
    def detect_faces(self, frame):
        """Fallback face detection using OpenCV"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        detections = []
        for (x, y, w, h) in faces:
            detections.append({
                'bbox': [x, y, w, h],
                'confidence': 0.9,
                'class_id': 0,
                'class_name': 'face'
            })
        
        return detections
    
    def update_tracking(self, detections):
        """Update object tracking using simple tracking algorithm"""
        current_tracks = {}
        
        for detection in detections:
            bbox = detection['bbox']
            center_x = bbox[0] + bbox[2] // 2
            center_y = bbox[1] + bbox[3] // 2
            
            # Find closest existing track
            min_distance = float('inf')
            best_track_id = None
            
            for track_id, track_info in self.trackers.items():
                if track_info['active']:
                    track_center = track_info['center']
                    distance = np.sqrt((center_x - track_center[0])**2 + (center_y - track_center[1])**2)
                    
                    if distance < min_distance and distance < 100:  # Maximum distance threshold
                        min_distance = distance
                        best_track_id = track_id
            
            if best_track_id is not None:
                # Update existing track
                self.trackers[best_track_id]['center'] = (center_x, center_y)
                self.trackers[best_track_id]['bbox'] = bbox
                self.trackers[best_track_id]['class_name'] = detection['class_name']
                self.trackers[best_track_id]['confidence'] = detection['confidence']
                self.trackers[best_track_id]['last_seen'] = time.time()
                
                # Update track history
                if best_track_id not in self.track_history:
                    self.track_history[best_track_id] = deque(maxlen=self.max_history)
                self.track_history[best_track_id].append((center_x, center_y))
                
                current_tracks[best_track_id] = self.trackers[best_track_id]
            else:
                # Create new track
                self.track_id += 1
                self.trackers[self.track_id] = {
                    'center': (center_x, center_y),
                    'bbox': bbox,
                    'class_name': detection['class_name'],
                    'confidence': detection['confidence'],
                    'last_seen': time.time(),
                    'active': True
                }
                
                self.track_history[self.track_id] = deque(maxlen=self.max_history)
                self.track_history[self.track_id].append((center_x, center_y))
                
                current_tracks[self.track_id] = self.trackers[self.track_id]
        
        # Mark inactive tracks
        current_time = time.time()
        for track_id in self.trackers:
            if track_id not in current_tracks:
                if current_time - self.trackers[track_id]['last_seen'] > 2.0:  # 2 seconds timeout
                    self.trackers[track_id]['active'] = False
        
        return current_tracks
    
    def draw_detections(self, frame, tracks):
        """Draw bounding boxes, labels, and tracking IDs"""
        for track_id, track_info in tracks.items():
            if not track_info['active']:
                continue
            
            bbox = track_info['bbox']
            x, y, w, h = bbox
            class_name = track_info['class_name']
            confidence = track_info['confidence']
            
            # Get color for this class
            class_id = 0  # Default to person
            if class_name in self.class_names:
                class_id = self.class_names.index(class_name)
            color = self.colors[class_id]
            
            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            
            # Draw label with tracking ID
            label = f"{class_name} #{track_id} ({confidence:.2f})"
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            
            # Draw label background
            cv2.rectangle(frame, (x, y - label_size[1] - 10), (x + label_size[0], y), color, -1)
            
            # Draw label text
            cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            # Draw tracking trail
            if track_id in self.track_history and len(self.track_history[track_id]) > 1:
                points = list(self.track_history[track_id])
                for i in range(1, len(points)):
                    cv2.line(frame, points[i-1], points[i], color, 2)
        
        return frame
    
    def process_video(self, source=0, output_path=None):
        """Process video stream with object detection and tracking"""
        # Open video source
        if isinstance(source, str):
            cap = cv2.VideoCapture(source)
        else:
            cap = cv2.VideoCapture(source)
        
        if not cap.isOpened():
            logger.error("Error opening video source")
            return
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        logger.info(f"Video source opened: {width}x{height} @ {fps}fps")
        
        # Setup video writer if output path is specified
        writer = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        start_time = time.time()
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # Detect objects
                detections = self.detect_objects(frame)
                
                # Update tracking
                tracks = self.update_tracking(detections)
                
                # Draw results
                frame = self.draw_detections(frame, tracks)
                
                # Add FPS and object count
                elapsed_time = time.time() - start_time
                current_fps = frame_count / elapsed_time if elapsed_time > 0 else 0
                
                info_text = f"FPS: {current_fps:.1f} | Objects: {len(tracks)}"
                cv2.putText(frame, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Write frame if output is specified
                if writer:
                    writer.write(frame)
                
                # Display frame
                cv2.imshow('Object Detection and Tracking', frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    # Save current frame
                    timestamp = int(time.time())
                    cv2.imwrite(f"frame_{timestamp}.jpg", frame)
                    logger.info(f"Frame saved as frame_{timestamp}.jpg")
        
        except KeyboardInterrupt:
            logger.info("Processing interrupted by user")
        
        finally:
            # Cleanup
            cap.release()
            if writer:
                writer.release()
            cv2.destroyAllWindows()
            
            logger.info(f"Processing completed. Processed {frame_count} frames")

def main():
    """Main function to run object detection and tracking"""
    parser = argparse.ArgumentParser(description='Object Detection and Tracking System')
    parser.add_argument('--source', type=str, default='0', 
                       help='Video source (0 for webcam, or path to video file)')
    parser.add_argument('--output', type=str, default=None,
                       help='Output video path (optional)')
    parser.add_argument('--model', type=str, default=None,
                       help='Path to YOLO model directory')
    parser.add_argument('--confidence', type=float, default=0.5,
                       help='Confidence threshold for detection')
    parser.add_argument('--nms', type=float, default=0.4,
                       help='Non-maximum suppression threshold')
    
    args = parser.parse_args()
    
    # Convert source to int if it's a number (webcam)
    try:
        source = int(args.source)
    except ValueError:
        source = args.source
    
    print("🎯 Object Detection and Tracking System")
    print("=" * 50)
    print(f"Source: {source}")
    print(f"Output: {args.output}")
    print(f"Model: {args.model}")
    print(f"Confidence: {args.confidence}")
    print(f"NMS: {args.nms}")
    print("\nControls:")
    print("- Press 'q' to quit")
    print("- Press 's' to save current frame")
    print("=" * 50)
    
    # Initialize tracker
    tracker = ObjectTracker(
        model_path=args.model,
        confidence_threshold=args.confidence,
        nms_threshold=args.nms
    )
    
    # Process video
    tracker.process_video(source=source, output_path=args.output)

if __name__ == "__main__":
    main() 