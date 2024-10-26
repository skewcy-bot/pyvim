import os
from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sys

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyvim.pyvim import VimEmulator
from typing import Dict


class PyVimWeb:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(current_dir, "templates")
        static_dir = os.path.join(current_dir, "static")

        print(f"Current directory: {current_dir}")
        print(f"Template directory: {template_dir}")
        print(f"Static directory: {static_dir}")

        self.app = Flask(
            __name__, template_folder=template_dir, static_folder=static_dir
        )

        CORS(self.app)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.vim_instances: Dict[str, VimEmulator] = {}

        self.setup_routes()
        self.setup_socketio()

    def setup_routes(self):
        @self.app.route("/")
        def index():
            return render_template("index.html")

        @self.app.route('/static/<path:filename>')
        def serve_static(filename):
            return send_from_directory(self.app.static_folder, filename)

    def setup_socketio(self):
        @self.socketio.on("connect")
        def handle_connect():
            session_id = request.sid
            self.vim_instances[session_id] = VimEmulator(
                "hello world\n", 0, 0, web_mode=True
            )
            emit("update", {"output": "Press any key to start"})

        @self.socketio.on("command")
        def handle_command(command):
            session_id = request.sid
            vim = self.vim_instances[session_id]
            output = vim.exec(command)
            emit("update", {"output": output})

    def run(self, debug=True, host="0.0.0.0", port=4399):
        self.socketio.run(self.app, debug=debug, host=host, port=port)
