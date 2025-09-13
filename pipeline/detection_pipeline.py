# pipeline/detection_pipeline.py

from models.text_classifier import TextClassifier
from models.audio_processor import AudioProcessor
from models.video_deepfake_detector import VideoDeepfakeDetector
import numpy as np
import cv2

# Initialize all our models once when the application starts
text_classifier = TextClassifier()
audio_processor = AudioProcessor()
video_detector = VideoDeepfakeDetector()

async def process_text_input(text: str) -> dict:
    """
    Orchestrates the analysis of a text input.
    """
    result = text_classifier.predict(text)
    return {
        "type": "text_analysis",
        "content": text,
        "result": result
    }

async def process_audio_input(audio_bytes: bytes, filename: str) -> dict:
    """
    Orchestrates the analysis of an audio input.
    """
    # For the demo, save the audio file temporarily to be processed
    temp_audio_path = f"data/audio/{filename}"
    with open(temp_audio_path, "wb") as f:
        f.write(audio_bytes)

    # 1. Transcribe the audio to get the text content
    transcribed_text = await audio_processor.transcribe_audio(audio_bytes)
    
    # 2. Analyze the transcribed text for scams
    text_analysis_result = text_classifier.predict(transcribed_text)
    
    # 3. Analyze the audio file for spoofing
    spoof_analysis_result = audio_processor.predict_spoof(temp_audio_path)

    return {
        "type": "audio_analysis",
        "filename": filename,
        "transcribed_text": transcribed_text,
        "text_analysis": text_analysis_result,
        "spoof_analysis": spoof_analysis_result
    }

def process_video_frame(frame_bytes: bytes) -> dict:
    """
    Orchestrates the analysis of a single video frame.
    """
    # Decode the image bytes into an OpenCV frame
    nparr = np.frombuffer(frame_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    result = video_detector.analyze_frame(frame)
    
    return {
        "type": "video_frame_analysis",
        "result": result
    }