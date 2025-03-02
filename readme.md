# TextGripper

TextGripper is a lightweight cross-platform application that captures copied text (Ctrl+C) and broadcasts it over WebSockets. It consists of a Python WebSocket server and a Python-based GUI client using Tkinter.

## 📌 Features
- **Clipboard Listener**: Detects `Ctrl + C` and broadcasts copied text.
- **WebSocket Server**: Sends clipboard text to connected clients.
- **Cross-Platform**: Works on Windows, Mac, and Linux.
- **GUI Client**: Displays received clipboard text in a user-friendly interface.
- **Automatic Reconnection**: Reconnects if WebSocket connection drops.

## 📂 Project Structure
```
TextGripper/
│── server/
│   ├── textgripper_server.py             # WebSocket Server (FastAPI)
│── client/
│   ├── textgripper_client.py             # Python GUI Client (Tkinter)
│── README.md                             # Documentation
│── requirements.txt                      # Dependencies
```

## 🛠️ Technologies Used
- **Python** (FastAPI, WebSockets, Tkinter)
- **Keyboard & Pyperclip** (Clipboard Monitoring)
- **AsyncIO** (Handling WebSocket Communication)

## 🚀 Installation & Setup
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/encryptedtouhid/TextGripper
cd TextGripper
```

### **2️⃣ Install Dependencies**
Ensure you have Python installed (>=3.8). Install dependencies:
```sh
pip install -r requirements.txt
```

### **3️⃣ Start the WebSocket Server**
```sh
python server/textgripper_server.py  
```
The server will start on `ws://localhost:8000/ws`

### **4️⃣ Run the GUI Client**
```sh
python client/textgripper_client.py 
```

## 📌 How It Works
1. **User presses `Ctrl + C`** → Text copied to clipboard
2. **Server detects clipboard change** → Broadcasts via WebSocket
3. **Client receives text** → Appends it to the text area
4. **Status updates** → Shows connected/disconnected state

## 🔄 Auto Start (Optional)
To run TextGripper on startup, create a script or add it to system startup settings:
- **Windows**: Add to Task Scheduler
- **Linux/Mac**: Use a cron job or systemd service

## 🛠️ Troubleshooting
- **WebSocket Not Connecting?** Ensure the server is running.
- **Clipboard Not Detected?** Run Python as Administrator.
- **Lag in Clipboard Capture?** Add a small delay before reading (`time.sleep(0.1)`).

## 📜 License
This project is licensed under the MIT License.

## 💡 Contributions
Feel free to fork and submit PRs to improve this project!

## 📧 Contact
For any issues or feature requests, open an issue on GitHub or contact `me@tuhidulhossain.com`.

