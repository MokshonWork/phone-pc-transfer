# phone-pc-transfer(Made using AI)

# Local File Transfer Server

A lightweight Flask-based web application for seamless file sharing and clipboard synchronization between devices on the same local network. Perfect for quickly transferring files between your computer and phone without cloud services.

## Features

- 📤 **File Upload & Download** - Share files between devices instantly
- 📋 **Shared Clipboard** - Sync text snippets across devices
- 📱 **QR Code Access** - Scan to connect from mobile devices
- 🌐 **Local Network Only** - No internet required, your data stays private
- 🗑️ **File Management** - Delete files directly from the web interface
- 💾 **Simple Storage** - All files stored in a local `shared` folder

## Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

## Installation

1. Clone this repository or download the source code:
```bash
git clone <your-repository-url>
cd <repository-folder>
```

2. Install required dependencies:
```bash
pip install flask qrcode[pil]
```

## Project Structure

```
.
├── app.py                 # Main Flask application
├── shared/               # Upload directory (auto-created)
└── templates/
    └── index.html        # Web interface template (you'll need to create this)
```

## Usage

1. Start the server:
```bash
python app.py
```

2. Access the application:
   - **From your computer:** Open `http://localhost:5000/`
   - **From your phone:** 
     - Scan the QR code displayed on the webpage, or
     - Manually enter the URL shown in the terminal (e.g., `http://192.168.1.100:5000/`)

3. Use the web interface to:
   - Upload files from any device
   - Download files to any device
   - Share text via the shared clipboard
   - Delete files you no longer need

## Configuration

You can modify these settings in `app.py`:

- **PORT**: Change the server port (default: 5000)
- **UPLOAD_FOLDER**: Change where files are stored (default: `./shared`)
- **app.secret_key**: Change the secret key for session security (recommended for production)

```python
PORT = 5000
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "shared")
app.secret_key = "change-this-secret-key"
```

## Important Notes

⚠️ **Security Warning**: This application is designed for use on trusted local networks only. It does not include authentication or encryption. Do not expose it to the internet without proper security measures.

- The server binds to `0.0.0.0`, making it accessible to all devices on your local network
- The shared clipboard resets when the server restarts
- All uploaded files are stored in the `shared` folder
- File names are preserved as uploaded (be careful with overwrites)

## Features Explained

### File Transfer
Upload files from any device and download them on another. Files appear in a sortable list on the homepage.

### Shared Clipboard
Copy text on one device and paste it on another. The clipboard content is displayed on the homepage and persists until the server restarts or is updated.

### QR Code
A QR code is automatically generated with your local network URL, making it easy to connect mobile devices without typing.

## Troubleshooting

**Can't connect from phone:**
- Ensure both devices are on the same Wi-Fi network
- Check if your firewall is blocking port 5000
- Try disabling VPN if active

**Wrong IP address in QR code:**
- The app auto-detects your local IP, but it may pick the wrong interface if you have multiple network adapters
- Manually check your IP address and update the URL

**Files not uploading:**
- Check folder permissions for the `shared` directory
- Ensure you have enough disk space

## Template Required

This application requires an `index.html` template file in a `templates` folder. The template should include:
- File upload form
- List of uploaded files with download/delete buttons
- Clipboard text area
- QR code image display

## License

This project is open source and available under the MIT License.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## Author

Your Name - Feel free to contact me!

---

**Enjoy seamless local file transfers! 🚀**
