import asyncio
import json
import uvicorn
from fastapi import FastAPI, WebSocket
from threading import Thread
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SERVER_IP = os.getenv("SERVER_IP", "0.0.0.0")  # Default to 0.0.0.0 if not set
SERVER_PORT = int(os.getenv("SERVER_PORT", 8000))

app = FastAPI()
clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        clients.remove(websocket)
    finally:
        clients.discard(websocket)

async def broadcast_text(text):
    disconnected_clients = set()
    for client in clients:
        try:
            await client.send_text(json.dumps({"text": text}))
        except:
            disconnected_clients.add(client)
    clients.difference_update(disconnected_clients)

def start_server():
    """Start WebSocket server using .env config"""
    uvicorn.run(app, host=SERVER_IP, port=SERVER_PORT)

if __name__ == "__main__":
    server_thread = Thread(target=start_server, daemon=True)
    server_thread.start()
    server_thread.join()
