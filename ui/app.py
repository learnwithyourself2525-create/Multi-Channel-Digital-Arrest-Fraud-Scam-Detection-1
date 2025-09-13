# ui/app.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from alerts.alert_manager import ConnectionManager
from pipeline.detection_pipeline import process_text_input, process_audio_input, process_video_frame
import json

app = FastAPI()

# Mount static files for CSS/JS
app.mount("/static", StaticFiles(directory="ui/static"), name="static")

# Initialize the connection manager for alerts
manager = ConnectionManager()

# --- HTML Frontend ---
# Serve the main HTML page from a template file
@app.get("/")
async def get():
    with open("ui/templates/index.html") as f:
        return HTMLResponse(f.read())

# --- API Endpoints ---

@app.post("/analyze/text")
async def analyze_text_endpoint(data: dict):
    text_content = data.get("text")
    if not text_content:
        return {"error": "No text provided"}, 400
    
    result = await process_text_input(text_content)
    await manager.broadcast(result)
    return {"status": "Text analysis triggered", "details": result}

@app.post("/analyze/audio")
async def analyze_audio_endpoint(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    result = await process_audio_input(audio_bytes, file.filename)
    await manager.broadcast(result)
    return {"status": "Audio analysis triggered", "details": result}

# --- WebSocket Endpoint for Real-Time Video ---

@app.websocket("/ws/video")
async def websocket_video_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Receive video frame as bytes from the client
            frame_bytes = await websocket.receive_bytes()
            
            # Process the frame
            result = process_video_frame(frame_bytes)
            
            # Broadcast the result to all clients
            if result["result"]["face_detected"]:
                await manager.broadcast(result)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected from video stream.")

# --- WebSocket Endpoint for General Alerts ---

@app.websocket("/ws/alerts")
async def websocket_alerts_endpoint(websocket: WebSocket):
    # This endpoint is just for receiving broadcasted alerts from text/audio analysis
    await manager.connect(websocket)
    try:
        # Keep the connection alive
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected from alerts.")