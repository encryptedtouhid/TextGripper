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
            msg = await websocket.receive_text()  # Keep connection alive
            print(f"Received message: {msg}")
    except:
        pass
    finally:
        clients.discard(websocket)  # Ensure proper cleanup
        print("Client disconnected")


async def broadcast_text(text):
    """Send received text to all connected clients."""
    print(f"Broadcasting: {text}")
    if not clients:
        print("No clients connected")
        return

    disconnected_clients = set()
    for client in clients:
        try:
            await client.send_text(json.dumps({"text": text}))  # Send data
        except:
            print(f"Error sending to client: {client}")
            disconnected_clients.add(client)

    # Remove disconnected clients
    clients.difference_update(disconnected_clients)


def start_server():
    """Start WebSocket server on AWS."""
    print("Starting WebSocket server on 0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    # Start the WebSocket server
    server_thread = Thread(target=start_server, daemon=True)
    server_thread.start()
    server_thread.join()
