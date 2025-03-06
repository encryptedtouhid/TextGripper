# TextGripper

TextGripper is a cross-platform application that captures copied text (Ctrl+C) and broadcasts it over WebSockets. It consists of a Python WebSocket server, a broadcaster application, and a Python-based GUI client using Tkinter.

## 📌 Features
- **Clipboard Listener:** Detects Ctrl + C and broadcasts copied text.
- **WebSocket Server:** Manages connections and forwards clipboard text to clients.
- **Broadcaster App:** Captures clipboard text and sends it to the server.
- **Cross-Platform:** Works on Windows, Mac, and Linux.
- **GUI Client:** Displays received clipboard text in a user-friendly interface.
- **Automatic Reconnection:** Reconnects if WebSocket connection drops.
- **Environment Configuration:** Uses `.env` file for easy configuration.

## 📂 Project Structure
```
TextGripper/
│── server/
│   ├── textgripper_server.py             # WebSocket Server (FastAPI)
│── broadcaster/
│   ├── textgripper_broadcaster.py        # Sends clipboard text to the server
│── client/
│   ├── textgripper_client.py             # Python GUI Client (Tkinter)
│── .env                                  # Configuration file (Server IP, Port)
│── README.md                             # Documentation
│── requirements.txt                      # Dependencies
```

## 🛠️ Technologies Used
- **Python** (FastAPI, WebSockets, Tkinter)
- **Keyboard & Pyperclip** (Clipboard Monitoring)
- **AsyncIO** (Handling WebSocket Communication)
- **dotenv** (Environment variable management)

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/encryptedtouhid/TextGripper
cd TextGripper
```

### 2️⃣ Install Dependencies
Ensure you have Python installed (>=3.8). Install dependencies:
```sh
pip install -r requirements.txt
```

### 3️⃣ Configure the Environment Variables
Create a `.env` file in the root directory and add:
```
SERVER_IP=your-public-ip
SERVER_PORT=8000
```
Replace `your-public-ip` with the actual server IP or domain.

### 4️⃣ Start the WebSocket Server
```sh
python server/textgripper_server.py  
```
The server will start on `ws://0.0.0.0:8000/ws`

### 5️⃣ Start the Broadcaster
Run this on the machine where you want to capture clipboard text:
```sh
python broadcaster/textgripper_broadcaster.py  
```

### 6️⃣ Run the GUI Client
On any machine that needs to receive clipboard text, run:
```sh
python client/textgripper_client.py
```

## 📌 How It Works
1. **User presses Ctrl + C** → Text copied to clipboard.
2. **Broadcaster detects clipboard change** → Sends it to the WebSocket server.
3. **Server receives the text** → Broadcasts it to all connected clients.
4. **Client receives the text** → Displays it in the GUI.
5. **Status updates** → Shows connected/disconnected state.

## 🔄 Auto Start (Optional)
To run TextGripper on startup, create a script or add it to system startup settings:
- **Windows:** Add to Task Scheduler.
- **Linux/Mac:** Use a cron job or systemd service.

## 🛠️ Troubleshooting
- **WebSocket Not Connecting?** Ensure the server is running and firewall allows traffic on port `8000`.
- **Clipboard Not Detected?** Run Python as Administrator.
- **Lag in Clipboard Capture?** Add a small delay before reading (`time.sleep(0.1)`).

## 📜 License
This project is licensed under the MIT License.

## 💡 Contributions
Feel free to fork and submit PRs to improve this project!

## 📧 Contact
For any issues or feature requests, open an issue on GitHub or contact me@tuhidulhossain.com.

