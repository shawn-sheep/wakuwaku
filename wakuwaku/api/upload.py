from flask import request, current_app, jsonify, send_from_directory
from werkzeug.utils import secure_filename

import os

from wakuwaku.api import bp

@bp.route("/upload", methods=["POST"])
def upload():
    """
    Upload a file.

    ---
    tags:
      - File Upload
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The file to upload.
    responses:
      200:
        description: The file was uploaded successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              description: Success message.
              example: uploaded successfully
            url:
              type: string
              description: URL of the uploaded file.
              example: /api/images/12345678-1234-5678-1234-567812345678.jpg
      400:
        description: Failed to upload the file.
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message.
              example: upload failed
    """
    file = request.files.get("file")
    if file:
        # 随机生成文件名
        from uuid import uuid4
        filename = str(uuid4()) + "." + file.filename.split(".")[-1]
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return jsonify({
            "message": "uploaded successfully",
            "url": "/api/images/" + filename
        }), 200
    else:
        return jsonify({"message": "upload failed"}), 400

@bp.route("/images/<path:filename>", methods=["GET"])
def get_image(filename):
    """
    Get an uploaded image by filename.

    ---
    tags:
      - File Upload
    parameters:
      - name: filename
        in: path
        type: string
        required: true
        description: The filename of the uploaded image.
    responses:
      200:
        description: The requested image file.
        content:
          image/*:
            schema:
              type: file
      404:
        description: The requested image file does not exist.
    """
    print(current_app.root_path)
    print(current_app.config['UPLOAD_FOLDER'], filename)
    return send_from_directory('static/upload', filename)