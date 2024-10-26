import os
from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sys

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyvim.pyvim import VimEmulator
from typing import Dict

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
vim_instances: Dict[str, VimEmulator] = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)


@socketio.on("connect")
def handle_connect():
    session_id = request.sid
    vim_instances[session_id] = VimEmulator("hello world\n", 0, 0, web_mode=True)
    emit("update", {"output": "Press any key to start"})


@socketio.on("command")
def handle_command(command):
    session_id = request.sid
    vim = vim_instances[session_id]
    output = vim.exec(command)
    emit("update", {"output": output})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    socketio.run(app, host="0.0.0.0", port=port)
