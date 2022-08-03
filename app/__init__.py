import os
import tempfile

from flask import Flask, jsonify, request, send_file
from werkzeug.utils import secure_filename

from . import tasks

app = Flask(__name__)
tmp = tempfile.gettempdir()


@app.route("/generate", methods=["POST"])
def generate_preview():
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        return jsonify({"error": "No file uploaded"}), 422

    file_name = secure_filename(uploaded_file.filename)
    file_path = os.path.join(tmp, file_name)

    blob = uploaded_file.read()
    with open(file_path, "wb") as file_in:
        file_in.write(blob)

    task = tasks.generate_preview_task.delay(file_name)
    return jsonify({"task_id": task.id})


@app.route("/status/<task_id>", methods=["GET"])
def generate_preview_status(task_id: str):
    task = tasks.generate_preview_task.AsyncResult(task_id)
    return jsonify({"status": task.state})


@app.route("/download/<task_id>", methods=["GET"])
def generate_preview_result(task_id: str):
    task = tasks.generate_preview_task.AsyncResult(task_id)

    if task.state == "SUCCESS":
        file_path = task.result
        return send_file(file_path, as_attachment=True)

    else:
        return jsonify({"error": "Not found"}), 404
