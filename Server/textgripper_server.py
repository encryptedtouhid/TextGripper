import asyncio
import json
from fastapi import FastAPI, WebSocket
from threading import Thread
import uvicorn

app = FastAPI()
clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handles WebSocket connections."""
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            _ = await websocket.receive_text()  # Keep connection alive
    except:
        pass
    finally:
        clients.discard(websocket)  # Ensure proper cleanup

async def broadcast_text(text):
    """Broadcast text to all connected clients."""
    disconnected_clients = set()
    for client in clients:
        try:
            await client.send_text(json.dumps({"text": text}))  # Send data
        except:
            disconnected_clients.add(client)

    # Remove disconnected clients
    clients.difference_update(disconnected_clients)

def start_server():
    """Start WebSocket server on AWS."""
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Start the WebSocket server
    server_thread = Thread(target=start_server, daemon=True)
    server_thread.start()
    server_thread.join()
