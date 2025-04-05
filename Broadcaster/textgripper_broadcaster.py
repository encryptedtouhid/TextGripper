import asyncio
import websockets
import pyperclip
import keyboard
import time
from dotenv import load_dotenv
import os
import threading
from pystray import Icon, MenuItem, Menu
from PIL import Image

# Load environment variables
load_dotenv()

SERVER_IP = os.getenv("SERVER_IP", "localhost")
SERVER_PORT = os.getenv("SERVER_PORT", "8000")
SERVER_URL = f"ws://{SERVER_IP}:{SERVER_PORT}/ws"

# Icon paths
CONNECTED_ICON_PATH = "assets/images/connected.ico"
DISCONNECTED_ICON_PATH = "assets/images/disconnected.ico"

# Global state
connected = False
icon = None
icon_visible = False

def load_icon(path):
    """Load an .ico file as an image."""
    try:
        return Image.open(path)
    except Exception as e:
        print(f"Error loading icon '{path}': {e}")
        return None

def update_icon(icon_path, tooltip):
    """Update tray icon with custom image and tooltip."""
    global icon, icon_visible
    icon_image = load_icon(icon_path)

    if not icon:
        icon = Icon("ClipboardBroadcaster")
        icon.menu = Menu(MenuItem("Quit", lambda icon, item: icon.stop()))

    if icon_image:
        icon.icon = icon_image
        icon.title = tooltip

    if not icon_visible:
        icon_visible = True
        threading.Thread(target=icon.run, daemon=True).start()

async def check_connection():
    """Try to connect to the WebSocket server."""
    global connected
    try:
        async with websockets.connect(SERVER_URL):
            connected = True
            update_icon(CONNECTED_ICON_PATH, "Connected to server")
    except Exception:
        connected = False
        update_icon(DISCONNECTED_ICON_PATH, "Disconnected")

def background_checker():
    """Continuously checks server connection status."""
    while True:
        asyncio.run(check_connection())
        time.sleep(5)

async def send_text(text):
    """Send clipboard text to WebSocket server."""
    global connected
    try:
        async with websockets.connect(SERVER_URL) as websocket:
            connected = True
            update_icon(CONNECTED_ICON_PATH, "Connected to server")
            print(f"Sending: {text}")
            await websocket.send(text)
            await asyncio.sleep(0.1)
    except Exception as e:
        connected = False
        update_icon(DISCONNECTED_ICON_PATH, f"Disconnected: {e}")
        print(f"Error: {e}")

def get_clipboard_text():
    try:
        time.sleep(0.1)
        return pyperclip.paste()
    except Exception as e:
        return f"Error: {str(e)}"

def clipboard_listener():
    """Listen for Ctrl+C to send clipboard content."""
    while True:
        keyboard.wait("ctrl+c")
        text = get_clipboard_text()
        if text:
            print(f"Broadcasting: {text}")
            asyncio.run(send_text(text))

if __name__ == "__main__":
    threading.Thread(target=background_checker, daemon=True).start()
    clipboard_listener()
