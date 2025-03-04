import asyncio
import json
from fastapi import FastAPI, WebSocket
from threading import Thread
import uvicorn

app = FastAPI()
clients = set()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handles WebSocket connections and listens for messages."""
    await websocket.accept()
    clients.add(websocket)
    print(f"Client connected: {websocket.client}")

    try:
        while True:
            data = await websocket.receive_text()  # Keep connection alive
            print(f"Received message from broadcaster: {data}")  # Debugging
            await broadcast_text(data)  # Forward to clients
    except Exception as e:
        print(f"Client disconnected: {e}")
    finally:
        clients.discard(websocket)  # Ensure cleanup


async def broadcast_text(text):
    """Send received text to all connected clients."""
    if not clients:
        print("No clients connected.")
        return

    print(f"Broadcasting to {len(clients)} clients: {text}")

    disconnected_clients = set()
    for client in clients:
        try:
            await client.send_text(json.dumps({"text": text}))
        except Exception as e:
            print(f"Error sending to client: {e}")
            disconnected_clients.add(client)

    # Remove disconnected clients
    clients.difference_update(disconnected_clients)


def start_server():
    """Start WebSocket server on AWS."""
    print("Starting WebSocket server on 0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


if __name__ == "__main__":
    # Start the WebSocket server
    server_thread = Thread(target=start_server, daemon=True)
    server_thread.start()
    server_thread.join()
