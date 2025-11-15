# 🖥️ Network Traffic Handler

### Real-time network monitor with retro CRT terminal aesthetic

Dependencies-ZERO Monitor network traffic in real-time with an authentic retro CRT terminal look. No external libraries required!

---

## ✨ Features

- 🖥️ **Retro CRT Design** - Green phosphor glow, scan lines, classic terminal feel
- 📊 **Real-time Monitoring** - Live traffic stats and message tracking
- 📱 **Mobile Friendly** - Control from any device on your network
- 🔄 **Dual Protocol** - Supports both WebSocket (browser) and TCP (Python)
- 🚀 **Zero Setup** - No pip install needed, pure Python!
- 🔒 **Multi-client** - Handle multiple connections simultaneously

***

## 📸 Screenshots

### Desktop Dashboard
<img src="https://drive.google.com/uc?export=view&id=1pkPHd1w170DSFKm0Gt4Nh3V3qbmq9G7b" width="800" alt="Dashboard">

### Mobile Client
<table>
  <tr>
    <td align="center">
      <img src="https://drive.google.com/uc?export=view&id=1Q8d2PSgALMUQMv_RDPH-XBC_FKk9Jo8D" width="300" alt="Mobile Connected"><br>
      <b>Connected</b>
    </td>
    <td align="center">
      <img src="https://drive.google.com/uc?export=view&id=1sXwpFULJHauvlgEQOh2X9-utPLBeJusR" width="300" alt="Mobile Disconnected"><br>
      <b>Disconnected</b>
    </td>
  </tr>
</table>

***

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/starlord78275/Network-Traffic-Handler.git
cd Network-Traffic-Handler

# No dependencies needed! 🎉
```

### Run the Server

```bash
python traffic_handler.py
```

**Output:**
```
🚀 TRAFFIC HANDLER SERVER STARTED
======================================================================
📊 Dashboard:      http://192.168.1.11:8080
📱 Mobile Client:  http://192.168.1.11:8080/mobile_client.html
💻 Local Access:   http://localhost:8080
======================================================================
```

### Access the Interface

| Device | URL |
|--------|-----|
| **Computer** | `http://localhost:8080` |
| **Phone/Tablet** | `http://YOUR_IP:8080/mobile_client.html` |

Replace `YOUR_IP` with the IP shown in your terminal.

***

## 💻 Usage

### Option 1: Python Client (Terminal)

```bash
python traffic_client.py
```

Then type messages:
```
Enter message (or "quit"): Hello!
[*] Server: ACK: Hello!
```

### Option 2: Mobile Client (Browser)

1. Open `http://YOUR_IP:8080/mobile_client.html` on your phone
2. Enter server IP
3. Click **"Connect"**
4. Send messages in real-time!

### Option 3: Multiple Devices

Connect from multiple phones, tablets, or terminals - all at once! Watch them all on the dashboard.

***

## 📂 Project Structure

```
Network-Traffic-Handler/
├── traffic_handler.py       # Main server
├── traffic_client.py         # Python test client
├── index.html                # Dashboard
├── style.css                 # Dashboard CRT styling
├── mobile_client.html        # Mobile interface
├── mobile_style.css          # Mobile CRT styling
├── app.js                    # Real-time updates
└── README.md                 # You are here!
```

***

## ⚙️ Configuration

### Change Ports

Edit `traffic_handler.py`:

```python
traffic_handler = TrafficHandler(tcp_port=9999)  # Traffic port
start_web_server(port=8080)                      # Web port
```

### Customize Colors

Edit `style.css` or `mobile_style.css`:

```css
:root {
    --crt-green: #00ff41;   /* Main color */
    --crt-amber: #ffb000;   /* Accent color */
}
```

### Windows Firewall

**Required for network access!**

Run PowerShell as Administrator:

```powershell
New-NetFirewallRule -DisplayName "Traffic Handler" -Direction Inbound -LocalPort 8080,9999 -Protocol TCP -Action Allow
```

***

## 🐛 Troubleshooting

### Can't connect from phone?

✅ Check both devices are on **same WiFi**  
✅ Use the **network IP** (not 127.0.0.1)  
✅ Make sure **firewall rules** are added  
✅ Server must be **running** when connecting  

### Port already in use?

**Windows:**
```bash
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -ti:8080 | xargs kill
```

Or change the port in `traffic_handler.py`.

***

## 🛠️ Technical Details

- **Backend**: Pure Python (`socket`, `threading`, `http.server`)
- **WebSocket**: Custom RFC 6455 implementation
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **No Dependencies**: 100% standard library

### How It Works

1. HTTP server serves the dashboard on port 8080
2. TCP server handles connections on port 9999
3. Auto-detects WebSocket vs raw TCP connections
4. Dashboard polls `/api/stats` every second for updates

***

## 🎨 Color Themes

Want different colors? Try these:

```css
/* Cyan Matrix */
--crt-green: #00ffff;
--crt-amber: #00ff00;

/* Red Alert */
--crt-green: #ff0000;
--crt-amber: #ff6600;

/* Purple Haze */
--crt-green: #ff00ff;
--crt-amber: #9933ff;

/* Classic Amber */
--crt-green: #ffb000;
--crt-amber: #ffd700;
```

***

## 🤝 Contributing

Found a bug? Want to add a feature? Contributions welcome!

1. Fork the repo
2. Create your branch (`git checkout -b feature/cool-feature`)
3. Commit changes (`git commit -m 'Add cool feature'`)
4. Push to branch (`git push origin feature/cool-feature`)
5. Open a Pull Request

***

## 📝 License

MIT License - free to use, modify, and distribute!

See [LICENSE](LICENSE) file for details.

***

## 🙏 Credits

- Built with Python's standard library
- Inspired by classic CRT terminals
- Font: [Share Tech Mono](https://fonts.google.com/specimen/Share+Tech+Mono) by Google Fonts

---

## 🎯 Roadmap

- [ ] TLS/SSL encryption
- [ ] User authentication
- [ ] Export logs to CSV
- [ ] Bandwidth graphs
- [ ] Multiple color themes
- [ ] Docker support

---

<div align="center">

**Made with 💚 by [starlord78275](https://github.com/starlord78275)**

⭐ **Star this repo if you like it!** ⭐

[Report Bug](https://github.com/starlord78275/Network-Traffic-Handler/issues) · [Request Feature](https://github.com/starlord78275/Network-Traffic-Handler/issues)

</div>
