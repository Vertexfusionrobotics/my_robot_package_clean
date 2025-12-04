"""
ARI Face Recognition System
Detects faces, recognizes people, and detects emotions using OpenCV only
"""
import cv2
import numpy as np
import os
import json
import time
from datetime import datetime
import pickle

FACE_RECOGNITION_AVAILABLE = True  # Using OpenCV, always available

class AriFaceRecognition:
    """Face recognition and emotion detection for ARI."""
    
    def __init__(self, mock_mode=False):
        self.camera = None
        self.camera_active = False
        self.mock_mode = mock_mode  # Simulate camera for testing
        self.known_faces = {}  # name -> list of face images
        self.known_emotions = ["happy", "sad", "neutral", "surprised"]
        self.faces_file = "ari_known_faces.pkl"
        self.last_seen = {}
        
        # OpenCV cascades and recognizer
        self.face_cascade = None
        self.eye_cascade = None
        self.smile_cascade = None
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.labels = {}  # name -> label_id
        self.reverse_labels = {}  # label_id -> name
        
        # Initialize cascades
        self.initialize_cascades()
        
        # Load known faces
        self.load_known_faces()
        
        if mock_mode:
            print("⚠️ Running in MOCK MODE - camera simulation active")
        
    def initialize_cascades(self):
        """Initialize OpenCV cascades"""
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            self.eye_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_eye.xml'
            )
            self.smile_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_smile.xml'
            )
        except Exception as e:
            print(f"⚠️ Error loading cascades: {e}")
        
    def initialize_camera(self):
        """Start the camera"""
        if self.camera_active:
            return True
            
        try:
            self.camera = cv2.VideoCapture(0)
            if self.camera.isOpened():
                self.camera_active = True
                print("✅ Camera initialized successfully")
                return True
            else:
                print("❌ Failed to open camera")
                return False
        except Exception as e:
            print(f"❌ Camera error: {e}")
            return False
    
    def stop_camera(self):
        """Stop the camera"""
        if self.camera:
            self.camera.release()
            self.camera_active = False
            print("📷 Camera stopped")
    
    def load_known_faces(self):
        """Load previously learned faces"""
        if os.path.exists(self.faces_file):
            try:
                with open(self.faces_file, 'rb') as f:
                    data = pickle.load(f)
                    # Handle both old and new formats
                    if isinstance(data, dict):
                        self.known_faces = data.get('faces', {})
                        self.labels = data.get('labels', {})
                        self.reverse_labels = data.get('reverse_labels', {})
                    else:
                        # Old format or corrupted
                        self.known_faces = {}
                        self.labels = {}
                        self.reverse_labels = {}
                print(f"✅ Loaded {len(self.known_faces)} known faces")
                # Retrain recognizer
                if self.known_faces:
                    self._train_recognizer()
            except Exception as e:
                print(f"⚠️ Could not load faces: {e}")
                self.known_faces = {}
                self.labels = {}
                self.reverse_labels = {}
    
    def save_known_faces(self):
        """Save learned faces to file"""
        try:
            data = {
                'faces': self.known_faces,
                'labels': self.labels,
                'reverse_labels': self.reverse_labels
            }
            with open(self.faces_file, 'wb') as f:
                pickle.dump(data, f)
            print(f"✅ Saved {len(self.known_faces)} faces")
        except Exception as e:
            print(f"⚠️ Could not save faces: {e}")
    
    def learn_face(self, name):
        """Learn a new person's face from camera using OpenCV"""
        # Check if running in mock mode or camera unavailable
        if self.mock_mode:
            print(f"📸 [MOCK] Simulating learning face for {name}...")
            # Create mock face data
            mock_face = np.random.randint(0, 255, (200, 200), dtype=np.uint8)
            if name not in self.labels:
                label_id = len(self.labels)
                self.labels[name] = label_id
                self.reverse_labels[label_id] = name
            if name not in self.known_faces:
                self.known_faces[name] = []
            self.known_faces[name].append(mock_face)
            self.save_known_faces()
            print(f"✅ [MOCK] Successfully 'learned' {name}'s face!")
            return True
        
        if not self.camera_active:
            if not self.initialize_camera():
                print("❌ Cannot start camera!")
                print("💡 TIP: Camera not available on this system.")
                print("   - Chromebook Linux may not have camera access")
                print("   - Try using a USB webcam")
                print("   - Or run ARI on a Raspberry Pi/PC with camera")
                return False
        
        print(f"📸 Learning face for {name}...")
        print("Look at the camera and press SPACE when ready, ESC to cancel")
        print("A window should appear - if you don't see it, check your taskbar!")
        
        face_samples = []
        window_name = "Learn Face - Press SPACE"
        
        try:
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window_name, 640, 480)
        except Exception as e:
            print(f"⚠️ Window creation warning: {e}")
        
        frame_count = 0
        while len(face_samples) < 5:  # Get 5 good samples
            ret, frame = self.camera.read()
            if not ret:
                print("⚠️ Cannot read from camera")
                time.sleep(0.1)
                continue
            
            frame_count += 1
            if frame_count % 30 == 0:
                print(f"📹 Camera is working - {len(face_samples)}/5 samples captured")
                
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            # Display frame
            display_frame = frame.copy()
            cv2.putText(display_frame, f"Learning: {name} ({len(face_samples)}/5)", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(display_frame, "Press SPACE when ready", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            # Draw rectangles around faces
            for (x, y, w, h) in faces:
                cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            try:
                cv2.imshow(window_name, display_frame)
            except Exception as e:
                print(f"⚠️ Display error: {e}")
            
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                print("❌ Cancelled by user")
                cv2.destroyAllWindows()
                return False
            elif key == 32:  # SPACE
                if len(faces) == 1:
                    (x, y, w, h) = faces[0]
                    face_roi = gray[y:y+h, x:x+w]
                    # Resize to consistent size
                    face_roi = cv2.resize(face_roi, (200, 200))
                    face_samples.append(face_roi)
                    print(f"✅ Captured sample {len(face_samples)}/5")
                elif len(faces) == 0:
                    print(f"⚠️ No face detected - move closer to camera")
                else:
                    print(f"⚠️ Found {len(faces)} faces, need exactly 1")
        
        cv2.destroyAllWindows()
        
        # Store face samples with a label
        if name not in self.labels:
            label_id = len(self.labels)
            self.labels[name] = label_id
            self.reverse_labels[label_id] = name
        
        # Store the face samples
        if name not in self.known_faces:
            self.known_faces[name] = []
        self.known_faces[name].extend(face_samples)
        
        # Retrain the recognizer with all known faces
        self._train_recognizer()
        
        self.save_known_faces()
        print(f"✅ Successfully learned {name}'s face!")
        return True
    
    def _train_recognizer(self):
        """Train the face recognizer with all known faces"""
        faces = []
        labels = []
        
        for name, face_list in self.known_faces.items():
            label_id = self.labels[name]
            for face_img in face_list:
                faces.append(face_img)
                labels.append(label_id)
        
        if faces:
            self.face_recognizer.train(faces, np.array(labels))
            print(f"✅ Trained recognizer with {len(faces)} samples from {len(self.known_faces)} people")
    
    def detect_presence(self):
        """Check if anyone is in front of the camera"""
        if not self.camera_active:
            return False
            
        ret, frame = self.camera.read()
        if not ret:
            return False
        
        # Convert to grayscale for faster detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Initialize cascade if needed
        if self.face_cascade is None:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        return len(faces) > 0
    
    def recognize_face(self):
        """Recognize who is in front of the camera using OpenCV
        Returns: (name, confidence, emotion)
        """
        if not self.camera_active:
            return None, 0.0, "neutral"
        
        ret, frame = self.camera.read()
        if not ret:
            return None, 0.0, "neutral"
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Find faces
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) == 0:
            return None, 0.0, "neutral"
        
        # Take the first face
        (x, y, w, h) = faces[0]
        face_roi = gray[y:y+h, x:x+w]
        face_roi = cv2.resize(face_roi, (200, 200))
        
        # Try to recognize
        name = None
        confidence = 0.0
        
        if len(self.known_faces) > 0:
            try:
                label, conf = self.face_recognizer.predict(face_roi)
                # Lower confidence value = better match in OpenCV
                # Typical threshold is around 50-70
                if conf < 70:
                    name = self.reverse_labels.get(label, None)
                    # Convert confidence to 0-1 scale (invert because lower is better)
                    confidence = max(0.0, 1.0 - (conf / 100.0))
            except:
                pass
        
        # Detect emotion from the face
        emotion = self.detect_emotion(frame, (x, y, w, h))
        
        return name, confidence, emotion
    
    def detect_emotion(self, frame, face_rect):
        """Simple emotion detection from face features
        Returns: emotion string (happy, sad, neutral, surprised)
        face_rect: (x, y, w, h) tuple
        """
        try:
            # Extract face region
            x, y, w, h = face_rect
            face_region = frame[y:y+h, x:x+w]
            face_gray = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
            
            # Detect smile
            smiles = self.smile_cascade.detectMultiScale(face_gray, 1.8, 20)
            
            # Detect eyes
            eyes = self.eye_cascade.detectMultiScale(face_gray, 1.3, 5)
            
            # Simple emotion logic
            if len(smiles) > 0:
                return "happy"
            elif len(eyes) > 2:
                return "surprised"
            else:
                return "neutral"
                
        except Exception as e:
            return "neutral"
    
    def get_frame(self):
        """Get current camera frame for display"""
        if not self.camera_active:
            return None
            
        ret, frame = self.camera.read()
        if ret:
            return frame
        return None
    
    def continuous_recognition(self, callback=None, interval=2.0):
        """Continuously recognize faces and call callback with results
        callback(name, emotion) is called when face is detected
        """
        import time
        
        if not self.camera_active:
            self.initialize_camera()
        
        last_check = 0
        
        while self.camera_active:
            current_time = time.time()
            
            # Check every interval seconds
            if current_time - last_check >= interval:
                if self.detect_presence():
                    name, confidence, emotion = self.recognize_face()
                    
                    if callback:
                        callback(name, emotion, confidence)
                    
                last_check = current_time
            
            time.sleep(0.1)


# Convenience functions
def test_camera():
    """Test if camera is working"""
    face_rec = AriFaceRecognition()
    if face_rec.initialize_camera():
        print("✅ Camera is working!")
        print("Press ESC to close")
        
        while True:
            frame = face_rec.get_frame()
            if frame is not None:
                cv2.imshow("Camera Test", frame)
            
            if cv2.waitKey(1) & 0xFF == 27:
                break
        
        cv2.destroyAllWindows()
        face_rec.stop_camera()
        return True
    else:
        print("❌ Camera not working")
        return False


if __name__ == "__main__":
    print("ARI Face Recognition System")
    print("1. Test Camera")
    print("2. Learn New Face")
    print("3. Test Recognition")
    
    choice = input("Choose option: ")
    
    if choice == "1":
        test_camera()
    elif choice == "2":
        name = input("Enter person's name: ")
        face_rec = AriFaceRecognition()
        face_rec.learn_face(name)
        face_rec.stop_camera()
    elif choice == "3":
        face_rec = AriFaceRecognition()
        face_rec.initialize_camera()
        print("Looking for faces... Press ESC to stop")
        
        while True:
            if face_rec.detect_presence():
                name, confidence, emotion = face_rec.recognize_face()
                if name:
                    print(f"👋 Hello {name}! You look {emotion} (confidence: {confidence:.2f})")
                else:
                    print(f"😊 I see someone who looks {emotion}, but I don't know your name yet!")
            
            if cv2.waitKey(1000) & 0xFF == 27:
                break
        
        face_rec.stop_camera()
