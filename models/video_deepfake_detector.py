# models/video_deepfake_detector.py

from deepface import DeepFace
import cv2
import numpy as np

class VideoDeepfakeDetector:
    def __init__(self):
        """
        Initializes the video deepfake detector.
        The models for deepface will be downloaded on first use.
        """
        print("Initializing VideoDeepfakeDetector...")
        # Pre-load a model to avoid delay on the first frame
        try:
            _ = DeepFace.extract_faces("models/init.py", enforce_detection=False)
            print("DeepFace models loaded.")
        except Exception as e:
            print(f"Could not pre-load DeepFace models: {e}")

    def analyze_frame(self, frame: np.ndarray) -> dict:
        """
        Analyzes a single video frame for deepfake/spoofing indicators.

        Args:
            frame (np.ndarray): A video frame from OpenCV (in BGR format).

        Returns:
            dict: Analysis result for the frame.
        """
        try:
            # The core of the detection using deepface's anti-spoofing feature
            face_objs = DeepFace.extract_faces(
                img_path=frame,
                detector_backend='opencv',
                enforce_detection=True, # We only care about frames with faces
                anti_spoofing=True
            )

            # For simplicity, we'll return the result for the first detected face
            if face_objs:
                face = face_objs
                is_real = face.get('is_real', False)
                confidence = face.get('confidence', 0)
                
                return {
                    "face_detected": True,
                    "is_real": is_real,
                    "confidence": round(confidence, 2),
                    "explanation": "Liveness check passed." if is_real else "Liveness check failed (potential spoof)."
                }

        except Exception:
            # This exception is often raised if no face is detected
            pass

        return {"face_detected": False}