import asyncio
import websockets
import json
import pyperclip
import keyboard
import time
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SERVER_IP = os.getenv("SERVER_IP", "localhost")
SERVER_PORT = os.getenv("SERVER_PORT", "8000")

SERVER_URL = f"ws://{SERVER_IP}:{SERVER_PORT}/ws"

async def send_text(text):
    """Send text to the WebSocket server."""
    try:
        async with websockets.connect(SERVER_URL) as websocket:
            print(f"Sending: {text}")
            await websocket.send(text)
            await asyncio.sleep(0.1)  # Ensure message is sent before closing
    except Exception as e:
        print(f"Error: {e}")

def get_clipboard_text():
    """Get text from the clipboard."""
    try:
        time.sleep(0.1)  # Delay to ensure clipboard updates before reading
        return pyperclip.paste()
    except Exception as e:
        return f"Error: {str(e)}"

def clipboard_listener():
    """Listens for Ctrl+C and sends clipboard text."""
    while True:
        keyboard.wait("ctrl+c")  # Wait for clipboard copy event
        text = get_clipboard_text()
        if text:
            print(f"Broadcasting: {text}")
            asyncio.run(send_text(text))

if __name__ == "__main__":
    clipboard_listener()
