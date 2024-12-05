import os
from flask import render_template, send_from_directory
from app import app, socketio
from .queue import add_task, cancel_queue_item, update_queue_state

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory(os.path.join(app.root_path, "static"), filename)

@app.route("/outputs/<path:filename>")
def serve_outputs(filename):
    return send_from_directory(os.path.join(app.root_path, "..", "outputs"), filename)

@socketio.on("connect")
def on_connect():
    print("Client Connected")
    update_queue_state()

@socketio.on("disconnect")
def on_disconnect():
    print("Client Disconnected")

@socketio.on("start_generation")
def on_start_generation(data):
    print("Adding request to queue.")
    add_task(data)

@socketio.on("cancel_queue_item")
def on_cancel_queue_item(data):
    index = data.get("index")
    if index is not None:
        print("Canceling queued request...")
        cancel_queue_item(index)
