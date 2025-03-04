import asyncio
import websockets
import json
import pyperclip
import keyboard  # Detect hotkeys
import time  # Delay for clipboard updates

SERVER_URL = "ws://YOUR_AWS_PUBLIC_IP:8000/ws"

async def send_text(text):
    """Send text to the WebSocket server."""
    try:
        async with websockets.connect(SERVER_URL) as websocket:
            await websocket.send(json.dumps({"text": text}))
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
