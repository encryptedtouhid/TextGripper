import asyncio
import json
import threading
from fastapi import FastAPI, WebSocket
from tkinter import Tk, Text, Button, END, Label, Scrollbar, RIGHT, Y, BOTH, LEFT, X
import uvicorn
from uvicorn.config import Config
from uvicorn.server import Server

# --- FastAPI + WebSocket ---

app = FastAPI()
clients = set()
server: Server = None


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        log(f"[INFO] New client attempting to connect: {websocket.client}")
        await websocket.accept()
        clients.add(websocket)
        log(f"[SUCCESS] Client connected: {websocket.client}")

        while True:
            try:
                data = await websocket.receive_text()
                log(f"[RECEIVED] From {websocket.client}: {data}")
                await broadcast_text(data)
            except Exception as recv_err:
                log(f"[ERROR] Receiving from {websocket.client}: {recv_err}")
                break

    except Exception as accept_err:
        log(f"[ERROR] Error during client connection: {accept_err}")
    finally:
        clients.discard(websocket)
        log(f"[INFO] Client disconnected and removed: {websocket.client}")


async def broadcast_text(text):
    log(f"[INFO] Preparing to broadcast: {text}")

    if not clients:
        log("[INFO] No clients connected. Broadcast skipped.")
        return

    disconnected = set()
    log(f"[INFO] Broadcasting to {len(clients)} clients.")

    for client in clients:
        try:
            await client.send_text(json.dumps({"text": text}))
            log(f"[SUCCESS] Message sent to {client.client}")
        except Exception as send_err:
            log(f"[ERROR] Failed to send to {client.client}: {send_err}")
            disconnected.add(client)

    if disconnected:
        log(f"[INFO] Removing {len(disconnected)} disconnected clients.")
        clients.difference_update(disconnected)
    else:
        log("[INFO] All clients sent successfully.")


# --- GUI Application ---

class WebSocketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WebSocket Server")
        self.root.geometry("700x500")

        # Responsive and icon-enhanced buttons
        self.start_button = Button(
            root,
            text="🚀 Start Server",
            font=("Segoe UI", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.start_server
        )
        self.start_button.pack(pady=10, padx=20, fill=X)

        self.stop_button = Button(
            root,
            text="🛑 Stop Server",
            font=("Segoe UI", 12, "bold"),
            bg="#F44336",
            fg="white",
            state="disabled",
            command=self.stop_server
        )
        self.stop_button.pack(pady=(0, 10), padx=20, fill=X)

        self.log_label = Label(root, text="Logs:", font=("Segoe UI", 11, "bold"))
        self.log_label.pack()

        self.text_log = Text(root, wrap="word", height=20, width=80, font=("Consolas", 10))
        self.text_log.pack(fill=BOTH, expand=True, padx=10)

        self.scrollbar = Scrollbar(root, command=self.text_log.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.text_log.config(yscrollcommand=self.scrollbar.set)

        self.server_thread = None

    def start_server(self):
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        def run_server():
            global server
            try:
                log("[INFO] Initializing WebSocket server...")
                config = Config(app=app, host="0.0.0.0", port=8000, log_level="error")
                server = Server(config=config)
                log("[STARTING] WebSocket server on 0.0.0.0:8000")
                asyncio.run(server.serve())
                log("[STOPPED] Server shut down gracefully.")
            except Exception as e:
                log(f"[ERROR] Server failed to start: {e}")

        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()

    def stop_server(self):
        if server and not server.should_exit:
            log("[INFO] Sending stop signal to server...")
            server.should_exit = True
        else:
            log("[INFO] Server is already stopped or was never started.")

        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def log(self, message):
        self.text_log.insert(END, message + "\n")
        self.text_log.see(END)


# --- Logging ---
def log(message):
    print(message)
    if gui:
        gui.log(message)


# --- Main ---
gui = None
if __name__ == "__main__":
    root = Tk()
    gui = WebSocketApp(root)
    root.mainloop()
