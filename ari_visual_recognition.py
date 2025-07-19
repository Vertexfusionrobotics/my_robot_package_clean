# ARI Master Brain - Emotionally Adaptive Humanoid AI
# Copyright (c) 2020–2025 Tyrell Murray (ATVOM LLC - Vertex Fusion Robotics)
#
# All rights reserved. This software is the original work of the author.
# Unauthorized reproduction, modification, or distribution is prohibited.
#
# For licensing inquiries, contact: tyrellmurray28@gmail.com
#!/usr/bin/env python3
"""
ARI Visual Recognition System - Computer Vision and Deep Learning
Implements facial recognition, object detection, and visual scene understanding
"""

import cv2
import numpy as np
import os
import json
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

try:
    import tensorflow as tf
    from tensorflow import keras
    try:
        import face_recognition
        FACE_RECOGNITION_AVAILABLE = True
    except ImportError:
        FACE_RECOGNITION_AVAILABLE = False
        print("⚠️ face_recognition library not available - using OpenCV only")
    VISION_AVAILABLE = True
    print("✅ Computer vision libraries available")
except ImportError as e:
    VISION_AVAILABLE = False
    FACE_RECOGNITION_AVAILABLE = False
    print(f"⚠️ Computer vision libraries not available: {e}")

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
    print("✅ MediaPipe available for advanced face detection")
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    print("⚠️ MediaPipe not available")

class ARIVisualRecognition:
    """
    Advanced visual recognition system for ARI.
    Handles face recognition, emotion detection, object recognition, and scene analysis.
    """
    
    def __init__(self, auto_start=False, gui_mode=False):
        self.face_cascade = None
        self.eye_cascade = None
        self.smile_cascade = None
        self.known_faces = {}
        self.face_encodings = {}
        self.emotion_model = None
        self.object_detection_model = None
        
        # Visual memory
        self.visual_memory = []
        self.recognized_people = {}
        self.scene_context = {}
        
        # MediaPipe components
        self.mp_face_detection = None
        self.mp_face_mesh = None
        self.mp_hands = None
        self.mp_pose = None
        
        # Camera control
        self.camera = None
        self.camera_active = False
        self.current_frame = None
        self.gui_mode = gui_mode
        
        # Only initialize vision systems, never auto-start camera
        self.initialize_vision_systems(auto_start=False)
        
    def initialize_vision_systems(self, auto_start=False):
        """Initialize all computer vision components"""
        print("🔍 Initializing ARI Visual Recognition System...")
        
        if not VISION_AVAILABLE:
            print("❌ Computer vision libraries not available")
            return False
            
        # Never start camera automatically in GUI mode
        if auto_start and self.gui_mode:
            print("⚠️ Auto-start disabled - camera will be started by GUI")
            auto_start = False
            
        try:
            # Initialize OpenCV cascades
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
            self.smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
            
            # Initialize MediaPipe if available
            if MEDIAPIPE_AVAILABLE:
                self.mp_face_detection = mp.solutions.face_detection
                self.mp_face_mesh = mp.solutions.face_mesh
                self.mp_hands = mp.solutions.hands
                self.mp_pose = mp.solutions.pose
                print("✅ MediaPipe components initialized")
            
            # Load or create emotion detection model
            self.load_emotion_model()
            
            # Load object detection model
            self.load_object_detection_model()
            
            # Load known faces database
            self.load_known_faces()
            
            # Load object detection model
            self.load_object_detection_model()
            
            print("✅ Visual recognition system initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing vision systems: {e}")
            return False
    
    def load_emotion_model(self):
        """Load or create emotion detection model"""
        emotion_model_path = "ari_neural_models/emotion_model.h5"
        
        if os.path.exists(emotion_model_path) and VISION_AVAILABLE:
            try:
                self.emotion_model = keras.models.load_model(emotion_model_path)
                print("✅ Loaded existing emotion detection model")
            except:
                self.create_emotion_model()
        else:
            self.create_emotion_model()
    
    def create_emotion_model(self):
        """Create a basic emotion detection model"""
        if not VISION_AVAILABLE:
            return
            
        try:
            # Simple CNN for emotion detection
            model = keras.Sequential([
                keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
                keras.layers.MaxPooling2D((2, 2)),
                keras.layers.Conv2D(64, (3, 3), activation='relu'),
                keras.layers.MaxPooling2D((2, 2)),
                keras.layers.Conv2D(64, (3, 3), activation='relu'),
                keras.layers.Flatten(),
                keras.layers.Dense(64, activation='relu'),
                keras.layers.Dropout(0.5),
                keras.layers.Dense(7, activation='softmax')  # 7 basic emotions
            ])
            
            model.compile(
                optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            
            self.emotion_model = model
            print("✅ Created new emotion detection model")
            
        except Exception as e:
            print(f"❌ Error creating emotion model: {e}")

    def load_object_detection_model(self):
        """Load pre-trained object detection model"""
        try:
            # Use MobileNet for lightweight object detection
            if VISION_AVAILABLE:
                from tensorflow.keras.applications import MobileNetV2
                from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
                
                self.object_detection_model = MobileNetV2(weights='imagenet')
                self.preprocess_input = preprocess_input
                self.decode_predictions = decode_predictions
                print("✅ Loaded MobileNetV2 for object detection")
                return True
        except Exception as e:
            print(f"⚠️ Could not load object detection model: {e}")
            
        return False

    def detect_faces(self, image):
        """Detect faces in an image using multiple methods"""
        faces = []
        
        if not VISION_AVAILABLE:
            return faces
            
        try:
            # Convert to grayscale for detection
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Method 1: OpenCV Haar Cascades
            opencv_faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )
            
            for (x, y, w, h) in opencv_faces:
                faces.append({
                    'method': 'opencv',
                    'bbox': [x, y, w, h],
                    'confidence': 0.8  # Approximate confidence
                })
            
            # Method 2: face_recognition library (if available)
            if FACE_RECOGNITION_AVAILABLE:
                face_locations = face_recognition.face_locations(image)
                for (top, right, bottom, left) in face_locations:
                    faces.append({
                        'method': 'face_recognition',
                        'bbox': [left, top, right-left, bottom-top],
                        'confidence': 0.9
                    })
            
            print(f"🔍 Detected {len(faces)} faces")
            return faces
            
        except Exception as e:
            print(f"❌ Error detecting faces: {e}")
            return []
    
    def recognize_person(self, image, face_bbox):
        """Recognize a specific person from a face crop"""
        if not VISION_AVAILABLE:
            return None
            
        try:
            x, y, w, h = face_bbox
            face_crop = image[y:y+h, x:x+w]
            
            # Generate face encoding based on available method
            if FACE_RECOGNITION_AVAILABLE:
                try:
                    face_encodings = face_recognition.face_encodings(face_crop)
                    if not face_encodings:
                        return None
                    face_encoding = face_encodings[0]
                except:
                    print("⚠️ Face recognition library error, using OpenCV fallback")
                    # Fall back to OpenCV method
                    gray_face = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
                    gray_face = cv2.resize(gray_face, (64, 64))
                    face_encoding = cv2.calcHist([gray_face], [0], None, [256], [0, 256]).flatten()
            else:
                # OpenCV histogram method
                gray_face = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
                gray_face = cv2.resize(gray_face, (64, 64))
                face_encoding = cv2.calcHist([gray_face], [0], None, [256], [0, 256]).flatten()
            
            # Compare with known faces
            best_match = None
            best_confidence = 0
            
            for person_name, known_encoding in self.face_encodings.items():
                try:
                    known_encoding = np.array(known_encoding)
                    
                    if FACE_RECOGNITION_AVAILABLE and hasattr(face_encoding, 'shape') and face_encoding.shape == known_encoding.shape and len(face_encoding) > 100:
                        # Use face_recognition comparison
                        matches = face_recognition.compare_faces([known_encoding], face_encoding)
                        if matches[0]:
                            distance = face_recognition.face_distance([known_encoding], face_encoding)[0]
                            confidence = 1.0 - distance
                        else:
                            confidence = 0
                    else:
                        # Use OpenCV histogram comparison
                        similarity = cv2.compareHist(face_encoding.astype(np.float32), 
                                                   known_encoding.astype(np.float32), 
                                                   cv2.HISTCMP_CORREL)
                        confidence = max(0, similarity)  # Ensure positive
                    
                    if confidence > best_confidence and confidence > 0.4:  # Lower threshold for OpenCV
                        best_confidence = confidence
                        best_match = person_name
                        
                except Exception as e:
                    print(f"⚠️ Error comparing with {person_name}: {e}")
                    continue
            
            if best_match:
                # Update metadata
                if best_match in self.known_faces:
                    self.known_faces[best_match]['last_seen'] = datetime.now().isoformat()
                    self.known_faces[best_match]['times_seen'] += 1
                    self.known_faces[best_match]['confidence_history'].append(best_confidence)
                    self.save_known_faces()
                
                return {
                    'name': best_match,
                    'confidence': best_confidence,
                    'timestamp': datetime.now().isoformat()
                }
            
            return None
            
        except Exception as e:
            print(f"❌ Error recognizing person: {e}")
            return None
    
    def detect_emotion(self, image, face_bbox):
        """Detect emotion from facial expression"""
        if not VISION_AVAILABLE or self.emotion_model is None:
            return None
            
        try:
            x, y, w, h = face_bbox
            face_crop = image[y:y+h, x:x+w]
            
            # Preprocess for emotion model
            face_gray = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
            face_resized = cv2.resize(face_gray, (48, 48))
            face_normalized = face_resized.astype('float32') / 255.0
            face_input = np.expand_dims(face_normalized, axis=0)
            face_input = np.expand_dims(face_input, axis=-1)
            
            # Predict emotion
            emotion_predictions = self.emotion_model.predict(face_input, verbose=0)
            emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
            
            emotion_idx = np.argmax(emotion_predictions[0])
            emotion_confidence = emotion_predictions[0][emotion_idx]
            
            return {
                'emotion': emotion_labels[emotion_idx],
                'confidence': float(emotion_confidence),
                'all_emotions': {
                    emotion_labels[i]: float(emotion_predictions[0][i]) 
                    for i in range(len(emotion_labels))
                }
            }
            
        except Exception as e:
            print(f"❌ Error detecting emotion: {e}")
            return None
    
    def detect_objects(self, frame):
        """Detect and classify objects in the frame"""
        if not VISION_AVAILABLE or self.object_detection_model is None:
            return []
        
        try:
            # Preprocess frame for object detection
            img = cv2.resize(frame, (224, 224))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = np.expand_dims(img, axis=0)
            img = self.preprocess_input(img)
            
            # Predict objects
            predictions = self.object_detection_model.predict(img, verbose=0)
            decoded = self.decode_predictions(predictions, top=5)[0]
            
            # Format results
            objects = []
            for (imagenet_id, label, score) in decoded:
                if score > 0.1:  # Only include confident predictions
                    objects.append({
                        'label': label.replace('_', ' '),
                        'confidence': float(score),
                        'category': 'object'
                    })
            
            return objects
            
        except Exception as e:
            print(f"❌ Error in object detection: {e}")
            return []

    def analyze_scene(self, image):
        """Analyze the overall scene for context"""
        scene_info = {
            'timestamp': datetime.now().isoformat(),
            'faces_detected': 0,
            'people_recognized': [],
            'emotions_detected': [],
            'scene_description': "",
            'lighting_quality': "unknown",
            'image_quality': "unknown",
            'objects_detected': []
        }
        
        if not VISION_AVAILABLE:
            return scene_info
            
        try:
            # Detect faces
            faces = self.detect_faces(image)
            scene_info['faces_detected'] = len(faces)
            
            # Analyze each face
            for face in faces:
                bbox = face['bbox']
                
                # Recognize person
                person = self.recognize_person(image, bbox)
                if person:
                    scene_info['people_recognized'].append(person)
                
                # Detect emotion
                emotion = self.detect_emotion(image, bbox)
                if emotion:
                    scene_info['emotions_detected'].append(emotion)
            
            # Detect objects
            objects = self.detect_objects(image)
            scene_info['objects_detected'] = objects
            
            # Analyze image quality
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)
            
            if brightness < 50:
                scene_info['lighting_quality'] = "dark"
            elif brightness > 200:
                scene_info['lighting_quality'] = "bright"
            else:
                scene_info['lighting_quality'] = "good"
            
            # Analyze image sharpness (Laplacian variance)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            if laplacian_var > 100:
                scene_info['image_quality'] = "sharp"
            elif laplacian_var > 30:
                scene_info['image_quality'] = "acceptable"
            else:
                scene_info['image_quality'] = "blurry"
            
            # Generate scene description
            description_parts = []
            if scene_info['faces_detected'] > 0:
                description_parts.append(f"{scene_info['faces_detected']} person(s) detected")
            
            if scene_info['people_recognized']:
                names = [p['name'] for p in scene_info['people_recognized']]
                description_parts.append(f"recognized: {', '.join(names)}")
            
            if scene_info['emotions_detected']:
                emotions = [e['emotion'] for e in scene_info['emotions_detected']]
                description_parts.append(f"emotions: {', '.join(set(emotions))}")
            
            if scene_info['objects_detected']:
                objects = [obj['label'] for obj in scene_info['objects_detected']]
                description_parts.append(f"objects: {', '.join(set(objects))}")
            
            scene_info['scene_description'] = "; ".join(description_parts)
            
            return scene_info
            
        except Exception as e:
            print(f"❌ Error analyzing scene: {e}")
            return scene_info
    
    def learn_new_face(self, image, person_name, face_bbox=None):
        """Learn a new person's face"""
        if not VISION_AVAILABLE:
            return False
            
        try:
            if face_bbox is None:
                # Auto-detect face
                faces = self.detect_faces(image)
                if not faces:
                    print("❌ No face detected for learning")
                    return False
                face_bbox = faces[0]['bbox']
            
            x, y, w, h = face_bbox
            face_crop = image[y:y+h, x:x+w]
            
            # Generate simple face encoding using histogram features (OpenCV fallback)
            face_encoding = None
            encoding_method = "opencv_histogram"
            
            if FACE_RECOGNITION_AVAILABLE:
                try:
                    import face_recognition
                    face_encodings = face_recognition.face_encodings(face_crop)
                    if face_encodings:
                        face_encoding = face_encodings[0]
                        encoding_method = "face_recognition"
                        print("✅ Using face_recognition library for encoding")
                    else:
                        print("⚠️ Face recognition library couldn't encode, using OpenCV fallback")
                except Exception as e:
                    print(f"⚠️ Face recognition library error: {e}, using OpenCV fallback")
            
            if face_encoding is None:
                # Simple OpenCV-based face "encoding" (histogram of face region)
                gray_face = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
                gray_face = cv2.resize(gray_face, (64, 64))  # Normalize size
                face_encoding = cv2.calcHist([gray_face], [0], None, [256], [0, 256]).flatten()
                print("✅ Using OpenCV histogram for face encoding")
            
            # Store the encoding
            if hasattr(face_encoding, 'tolist'):
                self.face_encodings[person_name] = face_encoding.tolist()
            elif isinstance(face_encoding, list):
                self.face_encodings[person_name] = face_encoding
            else:
                self.face_encodings[person_name] = face_encoding.tolist() if hasattr(face_encoding, 'tolist') else list(face_encoding)
            
            # Store metadata
            self.known_faces[person_name] = {
                'first_seen': datetime.now().isoformat(),
                'times_seen': 1,
                'last_seen': datetime.now().isoformat(),
                'confidence_history': [],
                'method': encoding_method
            }
            
            # Save to disk
            self.save_known_faces()
            
            print(f"✅ Learned new face: {person_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error learning new face: {e}")
            return False
    
    def start_camera(self, gui_mode=True):
        """Start or connect to a camera.
        In GUI mode, the camera should already be initialized by the GUI."""
        if self.gui_mode and gui_mode:
            # In GUI mode, we expect the camera to be set by the GUI
            if self.camera is None or not self.camera.isOpened():
                print("❌ Camera not initialized by GUI yet")
                return False
            self.camera_active = True
            return True

        """Start the camera for recognition"""
        if not VISION_AVAILABLE:
            print("❌ Computer vision not available")
            return False
            
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                print("❌ Could not open camera")
                return False
                
            # Set camera properties for better performance
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
                
            self.camera_active = True
            print("🎥 Camera activated successfully")
            
            # Test capture to ensure camera is working
            ret, test_frame = self.camera.read()
            if ret:
                if not gui_mode:  # Only show separate window if not in GUI mode
                    cv2.namedWindow('Camera Feed', cv2.WINDOW_NORMAL)
                print("📹 Camera feed confirmed - ready for vision tasks")
                return True
            else:
                print("❌ Camera activated but unable to capture frames")
                self.stop_camera()
                return False
            
        except Exception as e:
            print(f"❌ Error starting camera: {e}")
            return False
    
    def stop_camera(self):
        """Stop the camera"""
        try:
            if self.camera and self.camera.isOpened():
                self.camera.release()
                cv2.destroyAllWindows()
                self.camera_active = False
                print("📷 Camera stopped")
                return True
        except Exception as e:
            print(f"❌ Error stopping camera: {e}")
            return False
    
    def capture_frame(self):
        """Capture a single frame from the camera"""
        if not self.camera_active or not self.camera:
            print("❌ Camera not active")
            return None
            
        try:
            ret, frame = self.camera.read()
            if ret:
                self.current_frame = frame
                return frame
            else:
                print("❌ Could not capture frame")
                return None
        except Exception as e:
            print(f"❌ Error capturing frame: {e}")
            return None
    
    def detect_faces_from_camera(self):
        """Detect faces from current camera frame"""
        frame = self.capture_frame()
        if frame is None:
            return []
        
        faces = self.detect_faces(frame)
        if faces:
            print(f"👤 Detected {len(faces)} face(s)")
        else:
            print("👤 No faces detected")
        return faces
    
    def recognize_person_from_camera(self):
        """Recognize person from current camera frame"""
        frame = self.capture_frame()
        if frame is None:
            return None
        
        faces = self.detect_faces(frame)
        if not faces:
            print("👤 No faces detected for recognition")
            return None
        
        # Use the first detected face
        face = faces[0]
        person = self.recognize_person(frame, face['bbox'])
        
        if person:
            print(f"👋 Recognized: {person['name']} (confidence: {person['confidence']:.2f})")
        else:
            print("❓ Person not recognized")
        
        return person
    
    def learn_face_from_camera(self, person_name):
        """Learn a new person's face from the current camera frame"""
        if not VISION_AVAILABLE:
            print("❌ Vision system not available")
            return False
            
        try:
            # Capture current frame
            frame = self.capture_frame()
            if frame is None:
                print("❌ Could not capture frame from camera")
                return False
            
            # Detect faces in the frame
            faces = self.detect_faces(frame)
            if not faces:
                print("❌ No face detected in camera frame")
                return False
            
            if len(faces) > 1:
                print("⚠️ Multiple faces detected, using the first one")
            
            # Use the first detected face
            face_bbox = faces[0]['bbox']
            print(f"📸 Learning face for {person_name}...")
            
            # Use the existing learn_new_face method with the captured frame
            result = self.learn_new_face(frame, person_name, face_bbox)
            
            if result:
                print(f"✅ Successfully learned face for {person_name}")
                return True
            else:
                print(f"❌ Failed to learn face for {person_name}")
                return False
                
        except Exception as e:
            print(f"❌ Error learning face from camera: {e}")
            return False

    def analyze_emotion_from_camera(self):
        """Analyze emotion from current camera frame"""
        frame = self.capture_frame()
        if frame is None:
            return None
        
        faces = self.detect_faces(frame)
        if not faces:
            print("👤 No faces detected for emotion analysis")
            return None
        
        # Use enhanced emotion detection
        emotions = self.enhanced_emotion_detection(frame, [face['bbox'] for face in faces])
        
        if emotions:
            for i, emotion in enumerate(emotions):
                print(f"😊 Face {i+1} emotions:")
                if emotion['basic_emotion']:
                    print(f"   Basic: {emotion['basic_emotion']['emotion']} ({emotion['basic_emotion']['confidence']:.2f})")
                if emotion['cnn_emotion']:
                    print(f"   CNN: {emotion['cnn_emotion']['emotion']} ({emotion['cnn_emotion']['confidence']:.2f})")
            return emotions
        else:
            print("😐 Could not analyze emotion")
            return None

    def detect_objects_from_camera(self):
        """Detect objects in current camera frame"""
        frame = self.capture_frame()
        if frame is None:
            return []
        
        objects = self.detect_objects(frame)
        
        if objects:
            print(f"🔍 Detected {len(objects)} objects:")
            for obj in objects:
                print(f"   {obj['label']}: {obj['confidence']:.2f}")
        else:
            print("🔍 No objects detected")
        
        return objects

    def analyze_scene_from_camera(self):
        """Perform comprehensive scene analysis from camera"""
        frame = self.capture_frame()
        if frame is None:
            return {}
        
        scene_info = self.analyze_scene(frame)
        
        print("🎬 Scene Analysis:")
        print(f"   Scene type: {scene_info.get('scene_type', 'unknown')}")
        print(f"   Lighting: {scene_info.get('lighting', 'unknown')}")
        print(f"   Activity: {scene_info.get('activity', 'unknown')}")
        
        # Print face info
        faces = scene_info.get('faces', [{}])[0].get('locations', [])
        if faces:
            print(f"   Faces detected: {len(faces)}")
        
        # Print top objects
        objects = scene_info.get('objects', [])
        if objects:
            print(f"   Top objects: {', '.join([obj['label'] for obj in objects[:3]])}")
        
        # Print dominant colors
        colors = scene_info.get('colors', [])
        if colors:
            print(f"   Dominant colors: {', '.join([c['name'] for c in colors[:3]])}")
        
        return scene_info

    def analyze_colors_from_camera(self):
        """Analyze colors in current camera frame"""
        frame = self.capture_frame()
        if frame is None:
            return []
        
        colors = self.analyze_dominant_colors(frame)
        
        print("🎨 Color Analysis:")
        for color in colors:
            print(f"   {color['name']}: {color['percentage']:.1%} - RGB{color['rgb']}")
        
        return colors

    def get_visual_summary(self):
        """Get a comprehensive visual summary of current scene"""
        frame = self.capture_frame()
        if frame is None:
            return "Camera not available"
        
        try:
            summary_parts = []
            
            # Scene analysis
            scene_info = self.analyze_scene(frame)
            scene_type = scene_info.get('scene_type', 'unknown')
            lighting = scene_info.get('lighting', 'unknown')
            
            summary_parts.append(f"I can see a {scene_type} scene with {lighting} lighting")
            
            # Face analysis
            faces = scene_info.get('faces', [{}])[0].get('locations', [])
            if faces:
                if len(faces) == 1:
                    summary_parts.append("I see 1 person")
                else:
                    summary_parts.append(f"I see {len(faces)} people")
                
                # Try to recognize faces
                for i, face in enumerate(faces):
                    person = self.recognize_person(frame, face)
                    if person:
                        summary_parts.append(f"I recognize {person['name']}")
            
            # Object analysis
            objects = scene_info.get('objects', [])
            if objects:
                top_objects = [obj['label'] for obj in objects[:3]]
                summary_parts.append(f"I can see: {', '.join(top_objects)}")
            
            # Color analysis
            colors = scene_info.get('colors', [])
            if colors:
                dominant_color = colors[0]['name']
                summary_parts.append(f"The dominant color is {dominant_color}")
            
            return ". ".join(summary_parts) + "."
            
        except Exception as e:
            return f"I'm having trouble analyzing the visual scene: {e}"

    def load_known_faces(self):
        """Load known faces database from file"""
        try:
            faces_dir = "ari_user_profiles"
            if not os.path.exists(faces_dir):
                os.makedirs(faces_dir)
            
            faces_file = os.path.join(faces_dir, "known_faces.json")
            if os.path.exists(faces_file):
                with open(faces_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.known_faces = data.get('known_faces', {})
                    self.face_encodings = {}
                    
                    # Convert face encodings back to numpy arrays
                    for name, face_data in self.known_faces.items():
                        if 'encoding' in face_data:
                            self.face_encodings[name] = np.array(face_data['encoding'])
                            print(f"📁 Loaded encoding for {name} (length: {len(face_data['encoding'])})")
                        else:
                            print(f"⚠️ No encoding found for {name} in saved data")
                    
                    print(f"✅ Loaded {len(self.known_faces)} known faces with {len(self.face_encodings)} encodings")
            else:
                self.known_faces = {}
                self.face_encodings = {}
                print("📝 Created new faces database")
                
        except Exception as e:
            print(f"❌ Error loading known faces: {e}")
            import traceback
            traceback.print_exc()
            self.known_faces = {}
            self.face_encodings = {}

    def save_known_faces(self):
        """Save known faces database to file"""
        try:
            faces_dir = "ari_user_profiles"
            if not os.path.exists(faces_dir):
                os.makedirs(faces_dir)
            
            faces_file = os.path.join(faces_dir, "known_faces.json")
            
            # Convert numpy arrays to lists for JSON serialization
            save_data = {
                'known_faces': {},
                'timestamp': datetime.now().isoformat()
            }
            
            for name, face_data in self.known_faces.items():
                save_data['known_faces'][name] = face_data.copy()
                if name in self.face_encodings:
                    encoding = self.face_encodings[name]
                    # Convert encoding to list if it's a numpy array
                    if hasattr(encoding, 'tolist'):
                        save_data['known_faces'][name]['encoding'] = encoding.tolist()
                    elif isinstance(encoding, list):
                        save_data['known_faces'][name]['encoding'] = encoding
                    else:
                        save_data['known_faces'][name]['encoding'] = list(encoding)
                    print(f"💾 Saving encoding for {name} (length: {len(save_data['known_faces'][name]['encoding'])})")
                else:
                    print(f"⚠️ No encoding found for {name}")
            
            with open(faces_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved known faces database with {len(save_data['known_faces'])} faces")
            return True
            
        except Exception as e:
            print(f"❌ Error saving known faces: {e}")
            import traceback
            traceback.print_exc()
            return False

    def analyze_dominant_colors(self, frame):
        """Analyze dominant colors in the frame"""
        try:
            # Convert to RGB and reshape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pixels = rgb_frame.reshape(-1, 3)
            
            # Use k-means clustering to find dominant colors
            from sklearn.cluster import KMeans
            
            # Limit pixels for performance
            if len(pixels) > 10000:
                pixels = pixels[::len(pixels)//10000]
            
            kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            colors = []
            for i, color in enumerate(kmeans.cluster_centers_):
                colors.append({
                    'rgb': [int(c) for c in color],
                    'percentage': float(np.sum(kmeans.labels_ == i) / len(kmeans.labels_)),
                    'name': self.color_name(color)
                })
            
            return sorted(colors, key=lambda x: x['percentage'], reverse=True)
            
        except Exception as e:
            return [{'name': 'unknown', 'rgb': [128, 128, 128], 'percentage': 1.0}]

    def color_name(self, rgb):
        """Convert RGB to approximate color name"""
        r, g, b = rgb
        
        if r > 200 and g > 200 and b > 200:
            return "white"
        elif r < 50 and g < 50 and b < 50:
            return "black"
        elif r > g and r > b:
            return "red"
        elif g > r and g > b:
            return "green"
        elif b > r and b > g:
            return "blue"
        elif r > 150 and g > 150 and b < 100:
            return "yellow"
        elif r > 150 and b > 150 and g < 100:
            return "purple"
        elif r > 150 and g > 100 and b < 100:
            return "orange"
        else:
            return "mixed"

    def analyze_lighting(self, frame):
        """Analyze lighting conditions"""
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            mean_brightness = np.mean(gray)
            
            if mean_brightness < 50:
                return "dark"
            elif mean_brightness < 120:
                return "dim"
            elif mean_brightness < 180:
                return "normal"
            else:
                return "bright"
                
        except:
            return "unknown"

    def detect_activity(self, frame):
        """Basic activity detection (placeholder for motion detection)"""
        try:
            # This is a simple implementation - could be enhanced with motion vectors
            if hasattr(self, 'previous_frame') and self.previous_frame is not None:
                diff = cv2.absdiff(self.previous_frame, frame)
                gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                motion_level = np.mean(gray_diff)
                
                if motion_level > 30:
                    return "active"
                elif motion_level > 10:
                    return "slight_movement"
                else:
                    return "static"
            
            self.previous_frame = frame.copy()
            return "unknown"
            
        except:
            return "unknown"

    def classify_scene_type(self, scene_info):
        """Classify the type of scene based on analysis"""
        try:
            face_count = len(scene_info.get('faces', [{}])[0].get('locations', []))
            objects = scene_info.get('objects', [])
            lighting = scene_info.get('lighting', 'unknown')
            
            # Simple rule-based classification
            if face_count > 0:
                if face_count == 1:
                    return "portrait"
                elif face_count > 1:
                    return "group"
            
            # Check for common objects
            object_labels = [obj['label'].lower() for obj in objects]
            
            if any(word in ' '.join(object_labels) for word in ['computer', 'laptop', 'monitor', 'keyboard']):
                return "workspace"
            elif any(word in ' '.join(object_labels) for word in ['bed', 'pillow', 'blanket']):
                return "bedroom"
            elif any(word in ' '.join(object_labels) for word in ['kitchen', 'stove', 'refrigerator']):
                return "kitchen"
            elif lighting == "dark":
                return "low_light"
            else:
                return "general"
                
        except:
            return "unknown"

    def enhanced_emotion_detection(self, frame, face_locations=None):
        """Enhanced emotion detection with multiple approaches"""
        emotions = []
        
        try:
            if face_locations is None:
                face_locations = self.detect_faces(frame)
                face_locations = [face['bbox'] for face in face_locations]
            
            for (x, y, w, h) in face_locations:
                # Extract face region
                face_roi = frame[y:y+h, x:x+w]
                
                # Method 1: Basic emotion detection using facial features
                basic_emotion = self.detect_basic_emotion(face_roi)
                
                # Method 2: CNN-based emotion detection (if model is available)
                cnn_emotion = None
                if self.emotion_model:
                    cnn_emotion = self.cnn_emotion_detection(face_roi)
                
                # Method 3: MediaPipe-based emotion hints
                mediapipe_hints = None
                if MEDIAPIPE_AVAILABLE:
                    mediapipe_hints = self.mediapipe_emotion_hints(face_roi)
                
                # Combine results
                emotion_result = {
                    'location': (x, y, w, h),
                    'basic_emotion': basic_emotion,
                    'cnn_emotion': cnn_emotion,
                    'mediapipe_hints': mediapipe_hints,
                    'confidence': 0.5  # Default confidence
                }
                
                emotions.append(emotion_result)
            
            return emotions
            
        except Exception as e:
            print(f"❌ Error in emotion detection: {e}")
            return []

    def detect_basic_emotion(self, face_roi):
        """Basic emotion detection using OpenCV cascades"""
        try:
            gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
            
            # Detect smiles
            smiles = self.smile_cascade.detectMultiScale(gray, 1.8, 20)
            
            # Detect eyes
            eyes = self.eye_cascade.detectMultiScale(gray)
            
            # Simple rules for basic emotion
            if len(smiles) > 0:
                return {"emotion": "happy", "confidence": 0.7}
            elif len(eyes) < 2:
                return {"emotion": "squinting", "confidence": 0.5}
            else:
                return {"emotion": "neutral", "confidence": 0.6}
                
        except:
            return {"emotion": "unknown", "confidence": 0.1}

    def cnn_emotion_detection(self, face_roi):
        """CNN-based emotion detection"""
        if not self.emotion_model:
            return None
            
        try:
            # Preprocess face for emotion model
            gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, (48, 48))
            normalized = resized.astype('float32') / 255.0
            reshaped = normalized.reshape(1, 48, 48, 1)
            
            # Predict emotion
            prediction = self.emotion_model.predict(reshaped, verbose=0)
            
            emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
            emotion_idx = np.argmax(prediction[0])
            confidence = float(prediction[0][emotion_idx])
            
            return {
                "emotion": emotions[emotion_idx],
                "confidence": confidence,
                "all_scores": {emotions[i]: float(prediction[0][i]) for i in range(len(emotions))}
            }
            
        except Exception as e:
            print(f"❌ Error in CNN emotion detection: {e}")
            return None

    def mediapipe_emotion_hints(self, face_roi):
        """Use MediaPipe to get facial geometry hints for emotion"""
        if not MEDIAPIPE_AVAILABLE:
            return None
            
        try:
            # This is a placeholder for MediaPipe facial geometry analysis
            # Could be enhanced with landmark analysis for emotion detection
            return {"status": "mediapipe_analysis_placeholder"}
            
        except:
            return None

    def start_camera_recognition(self):
        """Start real-time camera recognition with visual display"""
        if not self.start_camera():
            print("❌ Failed to start camera")
            return False
            
        print("🎥 Starting real-time camera recognition...")
        print("📹 Camera window opened - Press 'q' to quit")
        
        try:
            while True:
                frame = self.capture_frame()
                if frame is None:
                    break
                
                # Detect faces and draw rectangles
                faces = self.detect_faces(frame)
                display_frame = frame.copy()
                
                for face in faces:
                    x, y, w, h = face['bbox']
                    # Draw rectangle around face
                    cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    
                    # Try to recognize person
                    person = self.recognize_person(frame, face['bbox'])
                    if person:
                        label = f"{person['name']} ({person['confidence']:.2f})"
                        cv2.putText(display_frame, label, (x, y-10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    else:
                        cv2.putText(display_frame, "Unknown", (x, y-10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                
                # Display the frame
                cv2.imshow('ARI Camera Feed', display_frame)
                
                # Check for quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except KeyboardInterrupt:
            print("\n🛑 Camera recognition stopped by user")
        except Exception as e:
            print(f"❌ Error in camera recognition: {e}")
        finally:
            self.stop_camera()
            cv2.destroyAllWindows()
            
        return True

    # ...existing code...

def main():
    """Test the visual recognition system"""
    print("🔍 Testing ARI Visual Recognition System")
    
    vision = ARIVisualRecognition()
    
    # Print system status
    summary = vision.get_visual_memory_summary()
    print(f"📊 System Status: {summary}")
    
    # Test camera if available
    test_camera = input("🎥 Test real-time camera recognition? (y/n): ").lower().strip()
    if test_camera == 'y':
        vision.start_camera_recognition()

if __name__ == "__main__":
    main()
