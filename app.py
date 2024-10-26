from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from pyvim.pyvim import VimEmulator
from typing import Dict

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins for SocketIO

vim_instances: Dict[str, VimEmulator] = {}


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect")
def handle_connect():
    session_id = request.sid
    vim_instances[session_id] = VimEmulator("hello world\n", 0, 0, web_mode=True)


@socketio.on("command")
def handle_command(command):
    session_id = request.sid
    vim = vim_instances[session_id]
    output = vim.exec(command)
    emit("update", {"output": output})


if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=4399)
