import os
import io
import socket

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
    send_file,
    flash,
)

import qrcode

# ====== Configuration ======
PORT = 5000
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "shared")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "change-this-secret-key"  # needed for flash messages

# Simple in-memory clipboard (resets when server restarts)
shared_clipboard = {"text": ""}


def get_local_ip() -> str:
    """
    Try to guess the local IP address of this machine on the LAN.
    Used to build the URL encoded in the QR code.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't actually need to reach 8.8.8.8, just used to pick an interface
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except OSError:
        # Fallback - may not work from phone, but at least something
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


# ====== Routes ======

@app.route("/", methods=["GET"])
def index():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    files = sorted(files)
    # Build the URL that the QR code will encode
    ip = get_local_ip()
    transfer_url = f"http://{ip}:{PORT}/"
    return render_template(
        "index.html",
        files=files,
        clipboard_text=shared_clipboard["text"],
        transfer_url=transfer_url,
    )


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("No file part in request.")
        return redirect(url_for("index"))

    file = request.files["file"]
    if file.filename == "":
        flash("No file selected.")
        return redirect(url_for("index"))

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)
    flash(f"Uploaded: {file.filename}")
    return redirect(url_for("index"))


@app.route("/download/<path:filename>", methods=["GET"])
def download_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"], filename, as_attachment=True
    )


@app.route("/delete/<path:filename>", methods=["POST"])
def delete_file(filename):
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        flash(f"Deleted: {filename}")
    else:
        flash("File not found.")
    return redirect(url_for("index"))


@app.route("/clipboard", methods=["POST"])
def update_clipboard():
    text = request.form.get("clipboard_text", "")
    shared_clipboard["text"] = text
    flash("Clipboard updated.")
    return redirect(url_for("index"))


@app.route("/qr-code.png", methods=["GET"])
def qr_code():
    """
    Generate a QR code image for the transfer URL.
    Phone can scan this to open the web UI.
    """
    ip = get_local_ip()
    transfer_url = f"http://{ip}:{PORT}/"

    img = qrcode.make(transfer_url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


if __name__ == "__main__":
    ip = get_local_ip()
    print(f"\nServer running…")
    print(f"PC can open:    http://localhost:{PORT}/")
    print(f"Phone can open: http://{ip}:{PORT}/")
    print("Or just scan the QR code shown on the page.\n")

    app.run(host="0.0.0.0", port=PORT, debug=True)
