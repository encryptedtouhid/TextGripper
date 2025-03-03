import asyncio
import websockets
import pyperclip
import json
from fastapi import FastAPI, WebSocket
from threading import Thread
import uvicorn
import keyboard  # For detecting hotkeys
import time  # To add a small delay

app = FastAPI()
clients = set()

def get_clipboard_text():
    """Get text from the clipboard."""
    try:
        time.sleep(0.1)  # Delay to ensure clipboard updates before reading
        text = pyperclip.paste()
        return text if text else "No text copied"
    except Exception as e:
        return f"Error: {str(e)}"

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        clients.remove(websocket)

async def broadcast_text(text):
    """Send the captured text to all connected clients."""
    disconnected_clients = set()
    for client in clients:
        try:
            await client.send_text(json.dumps({"text": text}))
        except:
            disconnected_clients.add(client)
    clients.difference_update(disconnected_clients)

def clipboard_listener():
    """Listen for Ctrl+C press and capture clipboard text."""
    while True:
        keyboard.wait("ctrl+c")  # Wait for Ctrl+C
        text = get_clipboard_text()
        print(f"Captured Text: {text}")  # Print the captured text
        asyncio.run(broadcast_text(text))

def start_server():
    uvicorn.run(app, host="192.168.1.15", port=8000)

# Start the WebSocket server in a separate thread
server_thread = Thread(target=start_server, daemon=True)
server_thread.start()

# Start the clipboard listener in a separate thread
clipboard_thread = Thread(target=clipboard_listener, daemon=True)
clipboard_thread.start()

# Keep the main thread running
clipboard_thread.join()
