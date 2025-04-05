import tkinter as tk
from tkinter import ttk
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
        self.root.geometry("650x500")
        self.root.configure(bg="#f3f3f3")
        self.root.resizable(False, False)

        # Style setup
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#f3f3f3", font=("Segoe UI", 11))
        style.configure("TFrame", background="#f3f3f3")
        style.configure("Status.TLabel", font=("Segoe UI", 12, "bold"))

        # Main Frame
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Status Label
        self.status_label = ttk.Label(main_frame, text="Status: Disconnected ❌", foreground="red", style="Status.TLabel")
        self.status_label.pack(pady=(0, 10), anchor="w")

        # Text area frame
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill="both", expand=True)

        # Scrollbar
        self.scrollbar = tk.Scrollbar(text_frame)
        self.scrollbar.pack(side="right", fill="y")

        # Line numbers
        self.line_numbers = tk.Text(
            text_frame,
            width=4,
            padx=4,
            takefocus=0,
            bd=0,
            bg="#ececec",
            fg="#555555",
            state="disabled",
            font=("Segoe UI", 11),
            yscrollcommand=self.scrollbar.set
        )
        self.line_numbers.pack(side="left", fill="y")

        # Main text area
        self.text_area = tk.Text(
            text_frame,
            wrap="word",
            font=("Segoe UI", 11),
            bd=0,
            bg="white",
            padx=10,
            pady=10,
            yscrollcommand=self.on_scroll
        )
        self.text_area.pack(side="left", fill="both", expand=True)

        self.scrollbar.config(command=self.sync_scroll)

        # Bind events
        self.text_area.bind("<KeyRelease>", self.update_line_numbers)
        self.text_area.bind("<MouseWheel>", self.update_line_numbers)
        self.text_area.bind("<Button-1>", self.update_line_numbers)
        self.text_area.bind("<Return>", self.update_line_numbers)

        # Start WebSocket in a thread
        self.ws_thread = threading.Thread(target=self.start_websocket, daemon=True)
        self.ws_thread.start()

    def update_line_numbers(self, event=None):
        """Update the line numbers in the sidebar with a new line and 4px (approx 2 spaces) indentation."""
        lines = int(self.text_area.index('end-1c').split('.')[0])
        indent = ""  # Approx. 4px with 'Segoe UI' font at size 11
        line_numbers_string = "\n" + "\n".join(f"{indent}{i}" for i in range(1, lines + 1))
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", line_numbers_string)
        self.line_numbers.config(state="disabled")

    def on_scroll(self, *args):
        """Sync scroll for both text and line number widgets."""
        self.line_numbers.yview(*args)
        self.text_area.yview(*args)

    def sync_scroll(self, *args):
        """Sync scrollbar with both widgets."""
        self.text_area.yview(*args)
        self.line_numbers.yview(*args)

    async def listen_websocket(self):
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
            await asyncio.sleep(5)
            await self.listen_websocket()

    def start_websocket(self):
        asyncio.run(self.listen_websocket())

    def append_text(self, text):
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.see(tk.END)
        self.update_line_numbers()

    def update_status(self, text, color):
        self.status_label.config(text=f"Status: {text}", foreground=color)

if __name__ == "__main__":
    root = tk.Tk()
    app = TextGripperClient(root)
    root.mainloop()
