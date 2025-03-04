import tkinter as tk
import asyncio
import websockets
import json
import threading
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SERVER_IP = os.getenv("SERVER_IP", "localhost")
SERVER_PORT = os.getenv("SERVER_PORT", "8000")

WS_URL = f"ws://{SERVER_IP}:{SERVER_PORT}/ws"

class TextGripperClient:
    def __init__(self, root):
        self.root = root
        self.root.title("TextGripper Client")
        self.root.geometry("500x400")

        # Status Label
        self.status_label = tk.Label(root, text="Status: Disconnected ❌", fg="red", font=("Arial", 12, "bold"))
        self.status_label.pack(pady=5)

        # Text Area
        self.text_area = tk.Text(root, wrap="word", height=15, width=50, font=("Arial", 12))
        self.text_area.pack(padx=10, pady=10)

        # Connect WebSocket in a thread
        self.ws_thread = threading.Thread(target=self.start_websocket, daemon=True)
        self.ws_thread.start()

    async def listen_websocket(self):
        """Connects to the WebSocket server and listens for incoming messages."""
        try:
            async with websockets.connect(WS_URL) as websocket:
                self.update_status("Connected ✅", "green")
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    text = data.get("text", "")

                    if text:
                        print(f"Received: {text}")
                        self.append_text(text)
        except Exception as e:
            self.update_status("Disconnected ❌", "red")
            print(f"WebSocket Error: {e}")

            # Try reconnecting after 5 seconds
            await asyncio.sleep(5)
            await self.listen_websocket()

    def start_websocket(self):
        """Runs the WebSocket client in an asyncio event loop."""
        asyncio.run(self.listen_websocket())

    def append_text(self, text):
        """Appends received text to the text area."""
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.see(tk.END)  # Auto-scroll to the latest text

    def update_status(self, text, color):
        """Updates the status label in the UI."""
        self.status_label.config(text=f"Status: {text}", fg=color)

# Start the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = TextGripperClient(root)
    root.mainloop()
